// Natural language rule-based NLP fallback engine
const parseWithRuleBasedNLP = (input) => {
  const original = input.trim();
  let text = original;

  // 1. Clean common trigger prefixes
  text = text.replace(/^(add task:?|create task:?|new task:?|remind me to|i need to|please|todo:?)\s*/i, '');

  // 2. Extract priority
  let priority = 'Medium';
  if (/\b(urgent|asap|critical|high\s+priority|highest\s+priority|urgent\s+priority|important)\b/i.test(text)) {
    priority = 'High';
    text = text.replace(/\b(with\s+)?(urgent|asap|critical|high|highest|urgent|important)(\s+priority)?\b/gi, '');
  } else if (/\b(low\s+priority|when\s+free|minor|trivial|lowest\s+priority)\b/i.test(text)) {
    priority = 'Low';
    text = text.replace(/\b(with\s+)?(low|minor|trivial|lowest)(\s+priority)?\b/gi, '');
  } else if (/\b(medium\s+priority|normal\s+priority)\b/i.test(text)) {
    priority = 'Medium';
    text = text.replace(/\b(with\s+)?(medium|normal)(\s+priority)?\b/gi, '');
  }
  // Strip any leftover dangling "priority" word
  text = text.replace(/\b(with\s+)?priority\b/gi, '');

  // 3. Extract Due Date
  let dueDate = null;
  const now = new Date();

  // Helper to format Date object into YYYY-MM-DD
  const formatDateStr = (d) => {
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  // Check 'day after tomorrow'
  if (/\b(day after tomorrow)\b/i.test(text)) {
    const target = new Date(now);
    target.setDate(target.getDate() + 2);
    dueDate = formatDateStr(target);
    text = text.replace(/\b(by\s+|on\s+|due\s+)?day after tomorrow\b/gi, '');
  }
  // Check 'tomorrow'
  else if (/\btomorrow\b/i.test(text)) {
    const target = new Date(now);
    target.setDate(target.getDate() + 1);
    dueDate = formatDateStr(target);
    text = text.replace(/\b(by\s+|on\s+|due\s+)?tomorrow\b/gi, '');
  }
  // Check 'today' or 'tonight'
  else if (/\b(today|tonight)\b/i.test(text)) {
    dueDate = formatDateStr(now);
    text = text.replace(/\b(by\s+|on\s+|due\s+)?(today|tonight)\b/gi, '');
  }
  // Check 'in X days'
  else if (/\bin\s+(\d+)\s+days?\b/i.test(text)) {
    const match = text.match(/\bin\s+(\d+)\s+days?\b/i);
    const daysToAdd = parseInt(match[1], 10);
    const target = new Date(now);
    target.setDate(target.getDate() + daysToAdd);
    dueDate = formatDateStr(target);
    text = text.replace(/\b(by\s+|due\s+)?in\s+\d+\s+days?\b/gi, '');
  }
  // Check specific day of week: (e.g. by Friday, on Monday, next Tuesday)
  else {
    const daysOfWeek = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
    const dayRegex = /\b(by\s+|on\s+|next\s+)?(sunday|monday|tuesday|wednesday|thursday|friday|saturday)\b/i;
    const match = text.match(dayRegex);
    if (match) {
      const targetDayName = match[2].toLowerCase();
      const targetDayIndex = daysOfWeek.indexOf(targetDayName);
      const currentDayIndex = now.getDay();
      let diff = targetDayIndex - currentDayIndex;
      if (diff <= 0) diff += 7; // Target next occurrence
      const target = new Date(now);
      target.setDate(target.getDate() + diff);
      dueDate = formatDateStr(target);
      text = text.replace(dayRegex, '');
    }
  }

  // 4. Extract time mentions (e.g. "at 4pm", "by 5:30 pm", "4pm", "11:00 am")
  let timeStr = '';
  const timeRegex = /\b(?:at|by)?\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm))\b/i;
  const timeMatch = text.match(timeRegex);
  if (timeMatch) {
    timeStr = timeMatch[1].toUpperCase();
    text = text.replace(timeRegex, '');
  }

  // 5. Clean up remaining title
  let cleanTitle = text
    .replace(/\b(by|at|on|due|with)\s*$/i, '')
    .replace(/^\s*(by|at|on|due|with)\s*/i, '')
    .replace(/\s{2,}/g, ' ')
    .trim();

  // If title was stripped too much, fallback to original
  if (!cleanTitle || cleanTitle.length < 2) {
    cleanTitle = original;
  }

  // Capitalize first letter
  cleanTitle = cleanTitle.charAt(0).toUpperCase() + cleanTitle.slice(1);

  let description = '';
  if (timeStr) {
    description = `Scheduled time: ${timeStr}`;
  }

  return {
    title: cleanTitle,
    description,
    priority,
    dueDate,
    status: 'Pending',
    source: 'Natural Language Engine'
  };
};

// @desc    Parse natural language input into structured task properties
// @route   POST /api/ai/parse-task
// @access  Private
const parseTaskWithAI = async (req, res) => {
  try {
    const { input } = req.body;

    if (!input || typeof input !== 'string' || input.trim() === '') {
      return res.status(400).json({ message: 'Input prompt is required for AI parsing' });
    }

    const trimmedInput = input.trim();
    const apiKey = process.env.GEMINI_API_KEY;

    // If Gemini API Key is configured, attempt LLM parsing
    if (apiKey) {
      try {
        const todayStr = new Date().toISOString().split('T')[0];
        const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        const currentDay = dayNames[new Date().getDay()];

        const prompt = `You are a helpful task manager AI assistant. Extract structured task properties from this user instruction: "${trimmedInput}".
Reference Date: Today is ${todayStr} (${currentDay}).
Return ONLY a valid JSON object matching this exact schema:
{
  "title": string (concise task title without extra timing prepositions),
  "description": string (extra details, time of day notes, or empty string),
  "priority": "High" | "Medium" | "Low",
  "dueDate": "YYYY-MM-DD" (or null if no date mentioned),
  "status": "Pending"
}`;

        const response = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: prompt }] }],
              generationConfig: {
                responseMimeType: 'application/json'
              }
            })
          }
        );

        if (response.ok) {
          const data = await response.json();
          const rawText = data?.candidates?.[0]?.content?.parts?.[0]?.text;
          if (rawText) {
            const parsed = JSON.parse(rawText);
            return res.json({
              success: true,
              task: {
                title: parsed.title || trimmedInput,
                description: parsed.description || '',
                priority: ['Low', 'Medium', 'High'].includes(parsed.priority) ? parsed.priority : 'Medium',
                dueDate: parsed.dueDate || null,
                status: 'Pending'
              },
              source: 'Gemini 1.5 Flash AI'
            });
          }
        } else {
          console.warn('Gemini API returned error status:', response.status);
        }
      } catch (geminiError) {
        console.warn('Gemini parsing failed, falling back to rule-based parser:', geminiError.message);
      }
    }

    // Fallback: Smart Rule-Based NLP Parser (guarantees fast, 100% offline-resilient parsing)
    const result = parseWithRuleBasedNLP(trimmedInput);
    return res.json({
      success: true,
      task: result,
      source: 'Natural Language Engine'
    });
  } catch (error) {
    console.error('AI parse task error:', error.message);
    res.status(500).json({ message: 'Server error processing natural language task' });
  }
};

module.exports = {
  parseTaskWithAI
};
