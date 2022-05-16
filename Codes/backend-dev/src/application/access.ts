import { TimestampFieldConfig } from "@keystone-6/core/fields";
import { BaseListTypeInfo } from "@keystone-6/core/types";
import { UserStatusType, UserRoleType as Role } from "@prisma/client";
export { Role }; 

// // export { Role, UserStatusType }
// export enum Permission {
//   canManageUser,
// }

// const cronAuthKey = process.env.CRON_AUTH_KEY
// export const accessFilter = ({ session, context }) => {
//   // if the user is an Admin, they can access all the records
//   if (session?.data.role === Role.ADMIN) return true
//   if (
//     context.req.headers?.cronAuthKey === cronAuthKey ||
//     context.req.query?.cronAuthKey === cronAuthKey
//   ) {
//     return true
//   }
//   // if the user is agent, filter for agents users
//   if (
//     session?.data.role === Role.AGENT &&
//     (session?.data.status === UserStatusType.active ||
//       session?.data.status === UserStatusType.inactive)
//   ) {
//     return { agent: { id: { equals: session?.itemId } } }
//   }
//   // if the user is User, filter for users
//   if (
//     session?.data.role === Role.USER &&
//     session?.data.status === UserStatusType.active &&
//     session?.data.agent?.status === UserStatusType.active
//   ) {
//     return { user: { id: { equals: session?.itemId } } }
//   }
//   return false
// }

// export const notificationCreateOperationFilter = ({ session, context }): boolean => {
//   if (
//     context?.req.headers?.cronAuthKey === cronAuthKey ||
//     context?.req?.query?.cronAuthKey === cronAuthKey
//   ) {
//     return true
//   }
//   return session?.itemId && session?.data.role === Role.ADMIN
// }
// export const notificationsFilter = ({ session, context }) => {
//   // if the user is an Admin, they can access all the records
//   if (
//     context.req.headers?.cronAuthKey === cronAuthKey ||
//     context.req.query?.cronAuthKey === cronAuthKey
//   ) {
//     return true
//   }
//   if (session?.data.role === Role.ADMIN) return true
//   // if the user is agent, filter for agents users
//   if (
//     session?.data.role === Role.AGENT &&
//     (session?.data.status === UserStatusType.active ||
//       session?.data.status === UserStatusType.inactive)
//   ) {
//     return { user: { id: { equals: session?.itemId } } }
//   }
//   // if the user is User, filter for users
//   return false
// }

// export const userFilter = ({ session, context }) => {
//   if (
//     context.req?.body?.variables?.operationName ===
//     'AuthenticateUserWithPassword'
//   ) {
//     return true
//   }
//   if (
//     context.req.headers?.cronAuthKey === cronAuthKey ||
//     context.req.query?.cronAuthKey === cronAuthKey
//   ) {
//     return true
//   }
//   // if the user is an Admin, they can access all the records
//   if (session?.data.role === Role.ADMIN) return true
//   // if the user is agent, filter for agents users
//   if (
//     session?.data.role === Role.AGENT &&
//     (session?.data.status === UserStatusType.active ||
//       session?.data.status === UserStatusType.inactive)
//   ) {
//     return {
//       OR: [
//         { agent: { id: { equals: session?.itemId } } },
//         { id: { equals: session?.itemId } }
//       ]
//     }
//   }
//   // if the user is User, filter for users
//   if (
//     session?.data.role === Role.USER &&
//     session?.data.status === UserStatusType.active &&
//     session?.data.agent?.status === UserStatusType.active
//   ) {
//     return { id: { equals: session?.itemId } }
//   }
//   return true
// }

// const checkPermission = (permission: Permission, role: Role | undefined) => {
//   if (!role) {
//     return false
//   }
//   const validations: { [key in Role]: Permission[] } = {
//     [Role.USER]: [],
//     [Role.AGENT]: [Permission.canManageUser],
//     [Role.ADMIN]: [Permission.canManageUser]
//   }
//   if (validations[role].includes(permission)) {
//     return true
//   }
//   return false
// }

// type SessionContext = {
//   session?: {
//     data: {
//       name: string
//       role: Role
//     }
//     itemId: string
//     listKey: string
//   }
// }
// type ItemContext = { item: any } & SessionContext

// export const isSignedIn = ({ session }: SessionContext) => {
//   return !!session
// }

// export const permissions = {
//   canManageUpload: ({ session }: SessionContext) =>
//     checkPermission(Permission.canManageUser, session?.data.role),
//   canManageUsers: ({ session }: SessionContext) =>
//     checkPermission(Permission.canManageUser, session?.data.role)
// }

// export const rules = {
//   canUseAdminUI: ({ session }: SessionContext) => {
//     return session?.data.role === Role.ADMIN
//   },
//   canReadContentList: ({ session }: SessionContext) => {
//     if (permissions.canManageUpload({ session })) return true
//     return { status: { equals: 'published' } }
//   },
//   canManageUser: ({ session, item }: ItemContext) => {
//     if (permissions.canManageUsers({ session })) return true
//     if (session?.itemId === item.id) return true
//     return false
//   },
//   canManageUserList: ({ session }: SessionContext) => {
//     if (permissions.canManageUsers({ session })) return true
//     if (!isSignedIn({ session })) return false
//     return { where: { id: { equals: session!.itemId } } }
//   }
// }

export const fieldOptions: TimestampFieldConfig<BaseListTypeInfo> = {
  access: {
    read: () => true,
    create: () => false,
    update: () => false,
  },
  ui: {
    createView: {
      fieldMode: "hidden",
    },
    itemView: {
      fieldMode: "read",
    },
  },
  graphql: { omit: ["update", "create"] },
};
