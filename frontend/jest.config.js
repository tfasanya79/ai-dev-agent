export default {
  transformIgnorePatterns: [
    "/node_modules/(?!(react-markdown|rehype-highlight|vfile|hast-util-to-jsx-runtime)/)"
  ],
  transform: {
    "^.+\\.[jt]sx?$": "babel-jest",
  },
};
