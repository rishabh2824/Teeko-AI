module.exports = function override(config, env) {
  if (config.devServer) {
    config.devServer.setupMiddlewares = (middlewares, devServer) => {
      // Add custom middleware logic here if needed
      console.log("Setting up middlewares...");

      return middlewares;
    };
  }
  return config;
};
