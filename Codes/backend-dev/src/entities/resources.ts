import {
  float,
  relationship,
  select,
  text,
  timestamp,
} from "@keystone-6/core/fields";
import { list } from "@keystone-6/core";
import { fieldOptions, Role } from "../application/access";
import { sumField, avgField, currentField } from "../lib/fields";

export const Resource = list({
  access: {
    operation: {
      query: ({ session }) => !!session.itemId,
      create: ({ session }) => session?.data.role === Role.admin,
      update: ({ session }) => session?.data.role === Role.admin,
      delete: ({ session }) => session?.data.role === Role.admin,
    },
  },
  fields: {
    name: text({
      isIndexed: "unique",
      validation: {
        isRequired: true,
      },
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
    capacity: float({
      defaultValue: 0,
      validation: {
        isRequired: true,
      },
    }),
    unit: select({
      type: "enum",
      options: [
        { label: "Litter", value: "ltr" },
        { label: "KW", value: "kw" },
      ],
      validation: {
        isRequired: true,
      },
      defaultValue: "ltr",
      ui: { displayMode: "select" },
    }),
    resourceCategory: select({
      type: "enum",
      options: [
        { label: "Water", value: "water" },
        { label: "Power", value: "power" },
        { label: "SewageTreatment", value: "sewage_treatment" },
      ],
      db: { map: "resourceCategory" },
      validation: {
        isRequired: true,
      },
      // defaultValue: "water",
      ui: { displayMode: "select" },
    }),
    devices: relationship({
      ref: "Device.resource",
      many: true,
    }),
    tenant: relationship({
      ref: "Tenant.resources",
      many: false,
    }),
    deviceReadSum: sumField("resourceId"),
    deviceReadAvg: avgField("resourceId"),
    deviceReadCurrent: currentField("resourceId"),
    createdAt: timestamp({ ...fieldOptions, defaultValue: { kind: "now" } }),
    updatedAt: timestamp({ ...fieldOptions, db: { updatedAt: true } }),
  },
});
