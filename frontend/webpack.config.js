const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const CopyPlugin = require("copy-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const Dotenv = require('dotenv-webpack');

const devMode = process.env.NODE_ENV !== "production";
const git_sha = process.env.GITHUB_SHA;

let config = {
    context: __dirname,
    mode: "development",
    entry: {app: './assets/app.js'},
    output: {
      path: path.resolve('./public/build/'),
      filename: "[name]-[hash].js",
      publicPath: "/build/",
      clean: true
    },
    devServer: {
        static: {
          directory: path.join(__dirname, 'public'),
        },
        compress: true,
        port: 3000,
        allowedHosts: [
            'frontend',
            'localhost',
            'host.docker.internal',
            '.profilr.forzamor.local',
        ],
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
          "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization"
        }
    },
    module: {
        rules: [
            // {
            //     test: /\.css$/i,
            //     use: [MiniCssExtractPlugin.loader, "css-loader"],
            //   },
            // {
            //     test: /\.s[ac]ss$/i,
            //     use: [
            //         // Creates `style` nodes from JS strings
            //         //   "style-loader",
            //       // Translates CSS into CommonJS
            //         "css-loader",
            //       "sass-loader",
            //       // Compiles Sass to CSS
            //     //   {
            //     //     loader: "sass-loader",
            //     //     options: {
            //     //       // Prefer `dart-sass`
            //     //       implementation: require("dart-sass"),
            //     //     },
            //     //   },
            //     ],
            // },
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                  MiniCssExtractPlugin.loader,
                  "css-loader",
                  "postcss-loader",
                  "sass-loader",
                ],
              },
          {
            test: /\.m?js$/,
            exclude: /(node_modules|bower_components)/,
            use: {
              loader: 'babel-loader',
              options: {
                presets: [
                    '@babel/preset-env'
                ]
              }
            }
          }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin(),
        new CopyPlugin({
            patterns: [
                {
                    from: './assets/images/*.*',
                    globOptions: {
                        patterns: "*.+(png|jpg|jpeg|svg)",
                    },
                    to: 'images/[path][name][ext]'
                },
                {
                    from: './assets/icons/*.svg',
                    to: 'icons/[path][name][ext]'
                }
            ],
        }),
        new Dotenv(),
        new BundleTracker({filename: './public/build/webpack-stats.json'})
    ],

}

module.exports = (env, argv) => {
    if (argv.mode === 'development') {
      config.devtool = 'source-map';
      config.output.filename = "[name].js";
    }

    if (argv.mode === 'production') {
    }

    return config;
};
