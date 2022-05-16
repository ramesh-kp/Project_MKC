import { relationship, select, text, timestamp } from "@keystone-6/core/fields";
import { list } from "@keystone-6/core";
import { fieldOptions } from "../application/access";
import { sumField, avgField, currentField } from "../lib/fields";

export const Tenant = list({
  fields: {
    name: text({ validation: { isRequired: true } }),
    location: text({ validation: { isRequired: true } }),
    description: text({ validation: { isRequired: true } }),
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
    owners: relationship({
      ref: "User.tenant",
      many: true,
    }),
    parents: relationship({
      ref: "User.subTenants",
      many: true,
    }),
    parent: relationship({
      ref: "Tenant.children",
      ui: { createView: { fieldMode: "hidden" } },
      // hooks: {
      //   resolveInput: ({ context }) => ({
      //     connect: { id: getAgentId(context) }
      //   })
      // }
    }),
    children: relationship({
      ref: "Tenant.parent",
      many: true,
    }),
    facilities: relationship({
      ref: "Facility.tenants",
      many: true,
    }),
    devices: relationship({
      ref: "Device.tenant",
      many: true,
    }),
    resources: relationship({
      ref: "Resource.tenant",
      many: true,
    }),
    deviceReadSum: sumField("tenantId"),
    deviceReadAvg: avgField("tenantId"),
    deviceReadCurrent: currentField("tenantId"),
    createdAt: timestamp({ ...fieldOptions, defaultValue: { kind: "now" } }),
    updatedAt: timestamp({ ...fieldOptions, db: { updatedAt: true } }),
  },
});
