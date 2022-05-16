/*
Welcome to the auth file! Here we have put a config to do basic auth in Keystone.

`createAuth` is an implementation for an email-password login out of the box.
`statelessSessions` is a base implementation of session logic.

For more on auth, check out: https://keystonejs.com/docs/apis/auth#authentication-api
*/

import { createAuth } from "@keystone-6/auth";
import { statelessSessions } from "@keystone-6/core/session";
import {
  sendWelcomeEmail,
  sendPasswordResetEmail,
} from "../services/emailService";

const sessionSecret = process.env.SESSION_SECRET;

if (!sessionSecret) {
  if (process.env.NODE_ENV === "production") {
    throw new Error(
      "The SESSION_SECRET environment variable must be set in production"
    );
  }
}

// Here we define how auth relates to our schemas.
// What we are saying here is that we want to use the list `User`, and to log in
// we will need their email and password.
const { withAuth } = createAuth({
  listKey: "User",
  identityField: "email",
  sessionData: "role status tenant { id }",
  secretField: "password",
  initFirstItem: {
    // If there are no items in the database, keystone will ask you to create
    // a new user, filling in these fields.
    fields: ["name", "email", "phone", "password"],
    itemData: {
      role: "admin", //Role.ADMIN,
      status: "active",
      createdAt: new Date(),
      updatedAt: new Date(),
    },
    skipKeystoneWelcome: true,
  },
  passwordResetLink: {
    sendToken: async ({ itemId, identity, token, context }) => {
      const user = await context.query.User.findOne({
        where: { id: itemId as string },
        query: "name password { isSet}",
      });
      if (!user) {
        throw new Error("User not found");
      }
      try {
        if (!user.password.isSet) {
          await sendWelcomeEmail(token, identity);
        } else {
          await sendPasswordResetEmail(token, identity);
        }
      } catch (e) {
        console.log(e);
      }
    },
    tokensValidForMins: 60,
  },
});

// This defines how long people will remain logged in for.
// This will get refreshed when they log back in.
const sessionMaxAge = 60 * 60 * 24 * 7; // 7 days

// This defines how sessions should work. For more details, check out: https://keystonejs.com/docs/apis/session#session-api
const session = statelessSessions({
  maxAge: sessionMaxAge,
  secret: sessionSecret!,
  sameSite: "strict",
});

export { withAuth, session };
