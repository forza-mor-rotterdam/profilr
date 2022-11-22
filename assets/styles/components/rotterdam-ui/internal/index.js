// Bootstrap dependencies
window.Popper = require('@popperjs/core'); // required for tooltip, popup...
require('bootstrap');

// not a real js file, just allows webpack to find files to package, including CSS
// https://webpack.js.org/loaders/css-loader/
import '../rotterdam-ui.scss' // include bootstrap css file with own modifications

// Your code here....
