// Middleware to restrict access to Admin users only
const requireAdmin = (req, res, next) => {
  // Check if user is attached to request and has 'Admin' role
  if (req.user && req.user.role === 'Admin') {
    next(); // User is Admin, allow access
  } else {
    res.status(403).json({ message: 'Access denied: Administrator privileges required' });
  }
};

module.exports = { requireAdmin };
