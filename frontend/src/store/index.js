import Vue from "vue";
import Vuex from "vuex";


Vue.use(Vuex);


export default new Vuex.Store({
    // Enable vuex strict mode on development
    strict: process.env.NODE_ENV !== 'production',

    // Enabled component stores
    modules: {
    },

    // Where stored datas will live
    state: {
    },

    // Shared computed properties
    getters: {
    },

    // Actions are in charge to perform tasks which provoke mutations
    actions: {
        //
        // Common HTTP error logger.
        //
        // TODO: Make 'console.log' conditionnal to development environment or
        //       at least remove every ones.
        //
        // From given axios error response, manage different error kind to
        // component store.
        //
        // @fields: list of available form field names, field errors that does
        //          not match any of available names will be ignored.
        // @errorObject: Error object as returned from axios
        // @module: Optional module namespace to call commit/dispatch. If not
        //          given means root store level.
        //
        error_logger({ commit }, { fields, errorObject, module }){
            var opts = {};
            if(module){
                module = module + "/";
            } else {
                module = "";
                opts = { root: true };
            }

            if (errorObject.response) {
                console.log("Status: http%s", errorObject.response.status);

                if(errorObject.response.status == 400) {
                    console.log("Error returned from form");
                    commit({
                        type: module + "update_errors",
                        names: fields,
                        fields: errorObject.response.data.data
                    }, opts);
                } else if (errorObject.response.status == 500) {
                    console.log("Error server");
                    commit({
                        type: module + "update_errors",
                        fields: {
                            "global": ["Internal Server Error"],
                        }
                    }, opts);
                } else if (errorObject.response.status == 404) {
                    commit({
                        type: module + "update_errors",
                        fields: {
                            "global": ["Not Found"],
                        }
                    });
                } else {
                    console.log("Undetermined error");
                    commit({
                        type: module + "update_errors",
                        fields: {
                            "global": [`Error http${errorObject.response.status} : ${errorObject.response.statusText}`],
                        }
                    }, opts);
                }
            } else if (errorObject.request) {
                // The request was made but no response was received
                console.log("Request error");
                commit({
                    type: module + "update_errors",
                    fields: {
                        "global": ["Server does not respond to request"],
                    }
                }, opts);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.log("Error", errorObject.message);
            }
        },
    },

    // State mutations
    mutations: {},
    }
});
