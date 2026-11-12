const jwt = require('jsonwebtoken');
const User = require('../models/User');

// Middleware to verify JWT token and protect private routes
const protect = async (req, res, next) => {
  let token;

  // Check if token exists in the Authorization header (Bearer <token>)
  if (
    req.headers.authorization &&
    req.headers.authorization.startsWith('Bearer')
  ) {
    try {
      // Extract the token part from 'Bearer <token>'
      token = req.headers.authorization.split(' ')[1];

      // Verify the token using secret key
      const decoded = jwt.verify(token, process.env.JWT_SECRET);

      // Find user by ID and attach to request object (exclude password)
      req.user = await User.findById(decoded.id).select('-password');

      if (!req.user) {
        return res.status(401).json({ message: 'User not found with this token' });
      }

      next(); // Proceed to the next middleware or controller
    } catch (error) {
      console.error('Token verification error:', error.message);
      return res.status(401).json({ message: 'Not authorized, token invalid or expired' });
    }
  }

  if (!token) {
    return res.status(401).json({ message: 'Not authorized, no token provided' });
  }
};

module.exports = { protect };
