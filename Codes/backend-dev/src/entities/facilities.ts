import { relationship, select, text, timestamp } from "@keystone-6/core/fields";
import { list } from "@keystone-6/core";
import { fieldOptions, Role } from "../application/access";
import { sumField, avgField, currentField } from "../lib/fields";

export const Facility = list({
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
    tenants: relationship({
      ref: "Tenant.facilities",
      many: true,
    }),
    devices: relationship({
      ref: "Device.facility",
      many: true,
    }),
    deviceReadSum: sumField("facilityId"),
    deviceReadAvg: avgField("facilityId"),
    deviceReadCurrent: currentField("facilityId"),
    createdAt: timestamp({ ...fieldOptions, defaultValue: { kind: "now" } }),
    updatedAt: timestamp({ ...fieldOptions, db: { updatedAt: true } }),
  },
});
