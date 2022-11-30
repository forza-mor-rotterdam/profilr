import { Application } from "@hotwired/stimulus"
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers"
import { GITHUB_SHA } from "./constants/environment";

const application = Application.start()
const context = require.context("./controllers", true, /\.js$/)
application.load(definitionsFromContext(context))
console.log("git hash: " + GITHUB_SHA);
window.Stimulus = application