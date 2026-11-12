const swaggerJsdoc = require('swagger-jsdoc');

// Swagger definition configuration
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'TaskFlow API Documentation',
      version: '1.0.0',
      description: 'API documentation for TaskFlow - Task Management System (MERN Stack College Project)',
      contact: {
        name: 'TaskFlow Development Team (Suraj, Arpan, Tejasvi)'
      }
    },
    servers: [
      {
        url: 'http://localhost:5001',
        description: 'Local Development Server'
      }
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
          description: 'Enter your JWT token in the format: Bearer <token>'
        }
      }
    }
  },
  // Path to the API docs (route files with JSDoc annotations)
  apis: ['./routes/*.js']
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);

module.exports = swaggerSpec;
