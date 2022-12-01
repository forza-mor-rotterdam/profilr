import { Application as StimulusApplication } from "@hotwired/stimulus"
import { start as TurboStart } from "@hotwired/turbo"
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers"
import { GITHUB_SHA } from "./constants/environment";

const application = StimulusApplication.start()
const context = require.context("./controllers", true, /\.js$/)
application.load(definitionsFromContext(context))
console.log("git hash: " + GITHUB_SHA);
window.Stimulus = application

// TurboStart()