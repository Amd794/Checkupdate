const path = require('path')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const ParallelUglifyPlugin = require('webpack-parallel-uglify-plugin');
const TerserPlugin = require("terser-webpack-plugin");
const webpack = require("webpack");
module.exports = {
  mode: 'none',
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      }
    ]
  }
}