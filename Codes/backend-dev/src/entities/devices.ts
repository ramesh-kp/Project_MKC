import { relationship, select, text, timestamp } from "@keystone-6/core/fields";
import { list } from "@keystone-6/core";
import { fieldOptions, Role } from "../application/access";
import { sumField, avgField, currentField } from "../lib/fields";

export const Device = list({
  access: {
    operation: {
      query: ({ session }) => !!session.itemId,
      create: ({ session }) => session?.data.role === Role.admin,
      update: ({ session }) => session?.data.role === Role.admin,
      delete: ({ session }) => session?.data.role === Role.admin,
    },
  },
  fields: {
    name: text({}),
    deviceId: text({
      isIndexed: "unique",
      validation: {
        isRequired: true,
      },
    }),
    deviceReads: relationship({
      ref: "DeviceRead.device",
      many: true,
    }),
    deviceReadSum: sumField("id"),
    deviceReadAvg: avgField("id"),
    deviceReadCurrent: currentField("id"),
    edgeDeviceId: text({
      validation: {
        isRequired: true,
      },
    }),
    portNumber: text({
      validation: {
        isRequired: true,
      },
    }),
    description: text({
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
      defaultValue: "active",
      db: { map: "status" },
      ui: { displayMode: "segmented-control" },
    }),
    tenant: relationship({
      ref: "Tenant.devices",
      many: false,
    }),
    facility: relationship({
      ref: "Facility.devices",
      many: false,
    }),
    resource: relationship({
      ref: "Resource.devices",
      many: false,
    }),
    deviceType: relationship({
      ref: "DeviceType.devices",
      many: false,
    }),
    createdAt: timestamp({ ...fieldOptions, defaultValue: { kind: "now" } }),
    updatedAt: timestamp({ ...fieldOptions, db: { updatedAt: true } }),
  },
});
