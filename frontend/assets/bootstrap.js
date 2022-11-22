// import { startStimulusApp } from '@symfony/stimulus-bridge';


// export const app = startStimulusApp(require.context(
//     '@symfony/stimulus-bridge/lazy-controller-loader!./controllers',
//     true,
//     /\.[jt]sx?$/
// ));

// import { Application } from '@hotwired/stimulus';
// import { definitionsFromContext } from '@hotwired/stimulus/webpack-helpers';

// import css
// import './../css/index.css'

// const application = Application.start();
// const context = require.context('./controllers', true, /\.js$/);
// application.load(definitionsFromContext(context));


import { Application } from "@hotwired/stimulus"
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers"

const application = Application.start()
const context = require.context("./controllers", true, /\.js$/)
application.load(definitionsFromContext(context))
window.Stimulus = application

