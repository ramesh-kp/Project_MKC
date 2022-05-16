/*
Welcome to Keystone! This file is what keystone uses to start the app.

It looks at the default export, and expects a Keystone config object.

You can find all the config options in our docs here: https://keystonejs.com/docs/apis/config
*/
import "dotenv/config";
import { config } from "@keystone-6/core";

// Look in the schema file for how we define our lists, and how users interact with them through graphql or the Admin UI
import { lists } from "./src/application/schema";

// Keystone auth is configured separately - check out the basic auth setup we are importing from our auth file.
import { withAuth, session } from "./src/application/auth";
const domain = process.env.NEXT_PUBLIC_VERCEL_URL ?? "http://localhost:3000";
const port = Number(process.env.PORT) || 4000;
export default withAuth(
  // Using the config function helps typescript guide you to the available options.
  config({
    // the db sets the database provider - we're using sqlite for the fastest startup experience
    db: {
      provider: "postgresql",
      url: process.env.DATABASE_URL ?? "",
    },
    // experimental: {
    //   generateNextGraphqlAPI: true,
    //   generateNodeAPI: true,
    // },
    server: {
      cors: {
        origin: [
          "https://studio.apollographql.com",
          domain,
          "http://40.81.240.197:3000",
          "https://qa.mkc.naicotech.com",
        ],
        credentials: true,
      },
      port,
      maxFileSize: 200 * 1024 * 1024,
      healthCheck: true,
    },
    // This config allows us to set up features of the Admin UI https://keystonejs.com/docs/apis/config#ui
    ui: {
      // For our starter, we check that someone has session data before letting them see the Admin UI.
      isAccessAllowed: (context) => !!context.session?.data,
    },
    graphql: {
      playground: "apollo",
    },
    lists,
    session,
  })
);