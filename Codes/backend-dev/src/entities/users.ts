import {
  password,
  relationship,
  select,
  text,
  timestamp,
} from "@keystone-6/core/fields";
import { list } from "@keystone-6/core";
import { fieldOptions } from "../application/access";

export const User = list({
  access: {
    operation: {
      query: ({ session }) => true, //!!session.itemId,
      create: ({ session }) => !!session.itemId,
      update: ({ session }) => !!session.itemId,
      delete: ({ session }) => !!session.itemId,
    },
  },
  fields: {
    name: text({
      validation: {
        isRequired: true,
      },
    }),
    email: text({
      isIndexed: "unique",
      validation: {
        isRequired: true,
      },
      access: {
        read: () => true,
      },
    }),
    phone: text({
      validation: {
        isRequired: true,
      },
    }),
    password: password({
      validation: {
        isRequired: true,
      },
    }),

    role: select({
      type: "enum",
      options: [
        { label: "MKC Admin", value: "admin" },
        { label: "Tenant Admin", value: "tenant" },
        { label: "User", value: "user" },
      ],
      defaultValue: "tenant",
      ui: { displayMode: "segmented-control" },
    }),

    status: select({
      type: "enum",
      options: [
        { label: "Blocked", value: "blocked" },
        { label: "Active", value: "active" },
        { label: "Inactive", value: "inactive" },
      ],
      db: { map: "status" },
      defaultValue: "active",
      ui: { displayMode: "segmented-control" },
    }),
    tenant: relationship({
      ref: "Tenant.owners",
      many: false,
    }),
    subTenants: relationship({
      ref: "Tenant.parents",
      many: true,
    }),
    createdAt: timestamp({ ...fieldOptions, defaultValue: { kind: "now" } }),
    updatedAt: timestamp({ ...fieldOptions, db: { updatedAt: true } }),
  },
});
