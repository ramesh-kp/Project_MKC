import {
  decimal,
  relationship,
  timestamp,
  select,
} from "@keystone-6/core/fields";
import { list } from "@keystone-6/core";
import { fieldOptions, Role } from "../application/access";

export const DeviceRead = list({
  access: {
    operation: {
      query: ({ session }) => !!session.itemId,
      create: ({ session }) => session?.data.role === Role.admin,
      update: ({ session }) => session?.data.role === Role.admin,
      delete: ({ session }) => session?.data.role === Role.admin,
    },
  },
  fields: {
    device: relationship({
      ref: "Device.deviceReads",
      many: false,
    }),
    value: decimal({
      validation: {
        isRequired: true,
      },
    }),
    createdAt: timestamp({ ...fieldOptions, defaultValue: { kind: "now" } }),
  },
});
