import {
  json,
  relationship,
  select,
  text,
  timestamp,
} from "@keystone-6/core/fields";
import { list } from "@keystone-6/core";
import { fieldOptions, Role } from "../application/access";
import { sumField, avgField, currentField } from "../lib/fields";

export const DeviceType = list({
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
    description: text({
      validation: {
        isRequired: true,
      },
    }),
    scale: json({
      defaultValue: { something: true },
    }),
    unit: select({
      type: "enum",
      options: [
        { label: "Litre", value: "ltr" },
        { label: "KW", value: "kw" },
      ],
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
    devices: relationship({
      ref: "Device.deviceType",
      many: true,
    }),
    deviceReadSum: sumField("deviceTypeId"),
    deviceReadAvg: avgField("deviceTypeId"),
    deviceReadCurrent: currentField("deviceTypeId"),
    createdAt: timestamp({ ...fieldOptions, defaultValue: { kind: "now" } }),
    updatedAt: timestamp({ ...fieldOptions, db: { updatedAt: true } }),
  },
});
