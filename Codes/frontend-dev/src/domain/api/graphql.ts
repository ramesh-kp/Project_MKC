import { GraphQLClient } from 'graphql-request';
import { RequestInit } from 'graphql-request/dist/types.dom';
import { useMutation, UseMutationOptions, useQuery, UseQueryOptions } from 'react-query';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };

function fetcher<TData, TVariables>(client: GraphQLClient, query: string, variables?: TVariables, headers?: RequestInit['headers']) {
  return async (): Promise<TData> => client.request<TData, TVariables>(query, variables, headers);
}
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  DateTime: any;
  Decimal: any;
  /** The `JSON` scalar type represents JSON values as specified by [ECMA-404](http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-404.pdf). */
  JSON: any;
};

export type AuthenticatedItem = User;

export type CreateInitialUserInput = {
  email?: InputMaybe<Scalars['String']>;
  name?: InputMaybe<Scalars['String']>;
  password?: InputMaybe<Scalars['String']>;
  phone?: InputMaybe<Scalars['String']>;
};

export type DateTimeNullableFilter = {
  equals?: InputMaybe<Scalars['DateTime']>;
  gt?: InputMaybe<Scalars['DateTime']>;
  gte?: InputMaybe<Scalars['DateTime']>;
  in?: InputMaybe<Array<Scalars['DateTime']>>;
  lt?: InputMaybe<Scalars['DateTime']>;
  lte?: InputMaybe<Scalars['DateTime']>;
  not?: InputMaybe<DateTimeNullableFilter>;
  notIn?: InputMaybe<Array<Scalars['DateTime']>>;
};

export type DecimalFilter = {
  equals?: InputMaybe<Scalars['Decimal']>;
  gt?: InputMaybe<Scalars['Decimal']>;
  gte?: InputMaybe<Scalars['Decimal']>;
  in?: InputMaybe<Array<Scalars['Decimal']>>;
  lt?: InputMaybe<Scalars['Decimal']>;
  lte?: InputMaybe<Scalars['Decimal']>;
  not?: InputMaybe<DecimalFilter>;
  notIn?: InputMaybe<Array<Scalars['Decimal']>>;
};

export type Device = {
  __typename?: 'Device';
  createdAt?: Maybe<Scalars['DateTime']>;
  description?: Maybe<Scalars['String']>;
  deviceId?: Maybe<Scalars['String']>;
  deviceReadAvg?: Maybe<Scalars['Float']>;
  deviceReadCurrent?: Maybe<Scalars['Float']>;
  deviceReadSum?: Maybe<Scalars['Float']>;
  deviceReads?: Maybe<Array<DeviceRead>>;
  deviceReadsCount?: Maybe<Scalars['Int']>;
  deviceType?: Maybe<DeviceType>;
  edgeDeviceId?: Maybe<Scalars['String']>;
  facility?: Maybe<Facility>;
  id: Scalars['ID'];
  name?: Maybe<Scalars['String']>;
  portNumber?: Maybe<Scalars['String']>;
  resource?: Maybe<Resource>;
  status?: Maybe<DeviceStatusType>;
  tenant?: Maybe<Tenant>;
  updatedAt?: Maybe<Scalars['DateTime']>;
};


export type DeviceDeviceReadAvgArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type DeviceDeviceReadCurrentArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type DeviceDeviceReadSumArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type DeviceDeviceReadsArgs = {
  orderBy?: Array<DeviceReadOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: DeviceReadWhereInput;
};


export type DeviceDeviceReadsCountArgs = {
  where?: DeviceReadWhereInput;
};

export type DeviceCreateInput = {
  description?: InputMaybe<Scalars['String']>;
  deviceId?: InputMaybe<Scalars['String']>;
  deviceReads?: InputMaybe<DeviceReadRelateToManyForCreateInput>;
  deviceType?: InputMaybe<DeviceTypeRelateToOneForCreateInput>;
  edgeDeviceId?: InputMaybe<Scalars['String']>;
  facility?: InputMaybe<FacilityRelateToOneForCreateInput>;
  name?: InputMaybe<Scalars['String']>;
  portNumber?: InputMaybe<Scalars['String']>;
  resource?: InputMaybe<ResourceRelateToOneForCreateInput>;
  status?: InputMaybe<DeviceStatusType>;
  tenant?: InputMaybe<TenantRelateToOneForCreateInput>;
};

export type DeviceManyRelationFilter = {
  every?: InputMaybe<DeviceWhereInput>;
  none?: InputMaybe<DeviceWhereInput>;
  some?: InputMaybe<DeviceWhereInput>;
};

export type DeviceOrderByInput = {
  createdAt?: InputMaybe<OrderDirection>;
  description?: InputMaybe<OrderDirection>;
  deviceId?: InputMaybe<OrderDirection>;
  edgeDeviceId?: InputMaybe<OrderDirection>;
  id?: InputMaybe<OrderDirection>;
  name?: InputMaybe<OrderDirection>;
  portNumber?: InputMaybe<OrderDirection>;
  status?: InputMaybe<OrderDirection>;
  updatedAt?: InputMaybe<OrderDirection>;
};

export type DeviceRead = {
  __typename?: 'DeviceRead';
  createdAt?: Maybe<Scalars['DateTime']>;
  device?: Maybe<Device>;
  id: Scalars['ID'];
  value?: Maybe<Scalars['Decimal']>;
};

export type DeviceReadCreateInput = {
  device?: InputMaybe<DeviceRelateToOneForCreateInput>;
  value?: InputMaybe<Scalars['Decimal']>;
};

export type DeviceReadManyRelationFilter = {
  every?: InputMaybe<DeviceReadWhereInput>;
  none?: InputMaybe<DeviceReadWhereInput>;
  some?: InputMaybe<DeviceReadWhereInput>;
};

export type DeviceReadOrderByInput = {
  createdAt?: InputMaybe<OrderDirection>;
  id?: InputMaybe<OrderDirection>;
  value?: InputMaybe<OrderDirection>;
};

export type DeviceReadRelateToManyForCreateInput = {
  connect?: InputMaybe<Array<DeviceReadWhereUniqueInput>>;
  create?: InputMaybe<Array<DeviceReadCreateInput>>;
};

export type DeviceReadRelateToManyForUpdateInput = {
  connect?: InputMaybe<Array<DeviceReadWhereUniqueInput>>;
  create?: InputMaybe<Array<DeviceReadCreateInput>>;
  disconnect?: InputMaybe<Array<DeviceReadWhereUniqueInput>>;
  set?: InputMaybe<Array<DeviceReadWhereUniqueInput>>;
};

export type DeviceReadUpdateArgs = {
  data: DeviceReadUpdateInput;
  where: DeviceReadWhereUniqueInput;
};

export type DeviceReadUpdateInput = {
  device?: InputMaybe<DeviceRelateToOneForUpdateInput>;
  value?: InputMaybe<Scalars['Decimal']>;
};

export type DeviceReadWhereInput = {
  AND?: InputMaybe<Array<DeviceReadWhereInput>>;
  NOT?: InputMaybe<Array<DeviceReadWhereInput>>;
  OR?: InputMaybe<Array<DeviceReadWhereInput>>;
  createdAt?: InputMaybe<DateTimeNullableFilter>;
  device?: InputMaybe<DeviceWhereInput>;
  id?: InputMaybe<IdFilter>;
  value?: InputMaybe<DecimalFilter>;
};

export type DeviceReadWhereUniqueInput = {
  id?: InputMaybe<Scalars['ID']>;
};

export type DeviceRelateToManyForCreateInput = {
  connect?: InputMaybe<Array<DeviceWhereUniqueInput>>;
  create?: InputMaybe<Array<DeviceCreateInput>>;
};

export type DeviceRelateToManyForUpdateInput = {
  connect?: InputMaybe<Array<DeviceWhereUniqueInput>>;
  create?: InputMaybe<Array<DeviceCreateInput>>;
  disconnect?: InputMaybe<Array<DeviceWhereUniqueInput>>;
  set?: InputMaybe<Array<DeviceWhereUniqueInput>>;
};

export type DeviceRelateToOneForCreateInput = {
  connect?: InputMaybe<DeviceWhereUniqueInput>;
  create?: InputMaybe<DeviceCreateInput>;
};

export type DeviceRelateToOneForUpdateInput = {
  connect?: InputMaybe<DeviceWhereUniqueInput>;
  create?: InputMaybe<DeviceCreateInput>;
  disconnect?: InputMaybe<Scalars['Boolean']>;
};

export enum DeviceStatusType {
  Active = 'active',
  Blocked = 'blocked',
  Inactive = 'inactive'
}

export type DeviceStatusTypeNullableFilter = {
  equals?: InputMaybe<DeviceStatusType>;
  in?: InputMaybe<Array<DeviceStatusType>>;
  not?: InputMaybe<DeviceStatusTypeNullableFilter>;
  notIn?: InputMaybe<Array<DeviceStatusType>>;
};

export type DeviceType = {
  __typename?: 'DeviceType';
  createdAt?: Maybe<Scalars['DateTime']>;
  description?: Maybe<Scalars['String']>;
  deviceReadAvg?: Maybe<Scalars['Float']>;
  deviceReadCurrent?: Maybe<Scalars['Float']>;
  deviceReadSum?: Maybe<Scalars['Float']>;
  devices?: Maybe<Array<Device>>;
  devicesCount?: Maybe<Scalars['Int']>;
  id: Scalars['ID'];
  name?: Maybe<Scalars['String']>;
  resourceCategory?: Maybe<DeviceTypeResourceCategoryType>;
  scale?: Maybe<Scalars['JSON']>;
  status?: Maybe<DeviceTypeStatusType>;
  unit?: Maybe<DeviceTypeUnitType>;
  updatedAt?: Maybe<Scalars['DateTime']>;
};


export type DeviceTypeDeviceReadAvgArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type DeviceTypeDeviceReadCurrentArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type DeviceTypeDeviceReadSumArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type DeviceTypeDevicesArgs = {
  orderBy?: Array<DeviceOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: DeviceWhereInput;
};


export type DeviceTypeDevicesCountArgs = {
  where?: DeviceWhereInput;
};

export type DeviceTypeCreateInput = {
  description?: InputMaybe<Scalars['String']>;
  devices?: InputMaybe<DeviceRelateToManyForCreateInput>;
  name?: InputMaybe<Scalars['String']>;
  resourceCategory?: InputMaybe<DeviceTypeResourceCategoryType>;
  scale?: InputMaybe<Scalars['JSON']>;
  status?: InputMaybe<DeviceTypeStatusType>;
  unit?: InputMaybe<DeviceTypeUnitType>;
};

export type DeviceTypeOrderByInput = {
  createdAt?: InputMaybe<OrderDirection>;
  description?: InputMaybe<OrderDirection>;
  id?: InputMaybe<OrderDirection>;
  name?: InputMaybe<OrderDirection>;
  resourceCategory?: InputMaybe<OrderDirection>;
  status?: InputMaybe<OrderDirection>;
  unit?: InputMaybe<OrderDirection>;
  updatedAt?: InputMaybe<OrderDirection>;
};

export type DeviceTypeRelateToOneForCreateInput = {
  connect?: InputMaybe<DeviceTypeWhereUniqueInput>;
  create?: InputMaybe<DeviceTypeCreateInput>;
};

export type DeviceTypeRelateToOneForUpdateInput = {
  connect?: InputMaybe<DeviceTypeWhereUniqueInput>;
  create?: InputMaybe<DeviceTypeCreateInput>;
  disconnect?: InputMaybe<Scalars['Boolean']>;
};

export enum DeviceTypeResourceCategoryType {
  Power = 'power',
  SewageTreatment = 'sewage_treatment',
  Water = 'water'
}

export type DeviceTypeResourceCategoryTypeNullableFilter = {
  equals?: InputMaybe<DeviceTypeResourceCategoryType>;
  in?: InputMaybe<Array<DeviceTypeResourceCategoryType>>;
  not?: InputMaybe<DeviceTypeResourceCategoryTypeNullableFilter>;
  notIn?: InputMaybe<Array<DeviceTypeResourceCategoryType>>;
};

export enum DeviceTypeStatusType {
  Active = 'active',
  Blocked = 'blocked',
  Inactive = 'inactive'
}

export type DeviceTypeStatusTypeNullableFilter = {
  equals?: InputMaybe<DeviceTypeStatusType>;
  in?: InputMaybe<Array<DeviceTypeStatusType>>;
  not?: InputMaybe<DeviceTypeStatusTypeNullableFilter>;
  notIn?: InputMaybe<Array<DeviceTypeStatusType>>;
};

export enum DeviceTypeUnitType {
  Kw = 'kw',
  Ltr = 'ltr'
}

export type DeviceTypeUnitTypeNullableFilter = {
  equals?: InputMaybe<DeviceTypeUnitType>;
  in?: InputMaybe<Array<DeviceTypeUnitType>>;
  not?: InputMaybe<DeviceTypeUnitTypeNullableFilter>;
  notIn?: InputMaybe<Array<DeviceTypeUnitType>>;
};

export type DeviceTypeUpdateArgs = {
  data: DeviceTypeUpdateInput;
  where: DeviceTypeWhereUniqueInput;
};

export type DeviceTypeUpdateInput = {
  description?: InputMaybe<Scalars['String']>;
  devices?: InputMaybe<DeviceRelateToManyForUpdateInput>;
  name?: InputMaybe<Scalars['String']>;
  resourceCategory?: InputMaybe<DeviceTypeResourceCategoryType>;
  scale?: InputMaybe<Scalars['JSON']>;
  status?: InputMaybe<DeviceTypeStatusType>;
  unit?: InputMaybe<DeviceTypeUnitType>;
};

export type DeviceTypeWhereInput = {
  AND?: InputMaybe<Array<DeviceTypeWhereInput>>;
  NOT?: InputMaybe<Array<DeviceTypeWhereInput>>;
  OR?: InputMaybe<Array<DeviceTypeWhereInput>>;
  createdAt?: InputMaybe<DateTimeNullableFilter>;
  description?: InputMaybe<StringFilter>;
  devices?: InputMaybe<DeviceManyRelationFilter>;
  id?: InputMaybe<IdFilter>;
  name?: InputMaybe<StringFilter>;
  resourceCategory?: InputMaybe<DeviceTypeResourceCategoryTypeNullableFilter>;
  status?: InputMaybe<DeviceTypeStatusTypeNullableFilter>;
  unit?: InputMaybe<DeviceTypeUnitTypeNullableFilter>;
  updatedAt?: InputMaybe<DateTimeNullableFilter>;
};

export type DeviceTypeWhereUniqueInput = {
  id?: InputMaybe<Scalars['ID']>;
  name?: InputMaybe<Scalars['String']>;
};

export type DeviceUpdateArgs = {
  data: DeviceUpdateInput;
  where: DeviceWhereUniqueInput;
};

export type DeviceUpdateInput = {
  description?: InputMaybe<Scalars['String']>;
  deviceId?: InputMaybe<Scalars['String']>;
  deviceReads?: InputMaybe<DeviceReadRelateToManyForUpdateInput>;
  deviceType?: InputMaybe<DeviceTypeRelateToOneForUpdateInput>;
  edgeDeviceId?: InputMaybe<Scalars['String']>;
  facility?: InputMaybe<FacilityRelateToOneForUpdateInput>;
  name?: InputMaybe<Scalars['String']>;
  portNumber?: InputMaybe<Scalars['String']>;
  resource?: InputMaybe<ResourceRelateToOneForUpdateInput>;
  status?: InputMaybe<DeviceStatusType>;
  tenant?: InputMaybe<TenantRelateToOneForUpdateInput>;
};

export type DeviceWhereInput = {
  AND?: InputMaybe<Array<DeviceWhereInput>>;
  NOT?: InputMaybe<Array<DeviceWhereInput>>;
  OR?: InputMaybe<Array<DeviceWhereInput>>;
  createdAt?: InputMaybe<DateTimeNullableFilter>;
  description?: InputMaybe<StringFilter>;
  deviceId?: InputMaybe<StringFilter>;
  deviceReads?: InputMaybe<DeviceReadManyRelationFilter>;
  deviceType?: InputMaybe<DeviceTypeWhereInput>;
  edgeDeviceId?: InputMaybe<StringFilter>;
  facility?: InputMaybe<FacilityWhereInput>;
  id?: InputMaybe<IdFilter>;
  name?: InputMaybe<StringFilter>;
  portNumber?: InputMaybe<StringFilter>;
  resource?: InputMaybe<ResourceWhereInput>;
  status?: InputMaybe<DeviceStatusTypeNullableFilter>;
  tenant?: InputMaybe<TenantWhereInput>;
  updatedAt?: InputMaybe<DateTimeNullableFilter>;
};

export type DeviceWhereUniqueInput = {
  deviceId?: InputMaybe<Scalars['String']>;
  id?: InputMaybe<Scalars['ID']>;
};

export type Facility = {
  __typename?: 'Facility';
  createdAt?: Maybe<Scalars['DateTime']>;
  deviceReadAvg?: Maybe<Scalars['Float']>;
  deviceReadCurrent?: Maybe<Scalars['Float']>;
  deviceReadSum?: Maybe<Scalars['Float']>;
  devices?: Maybe<Array<Device>>;
  devicesCount?: Maybe<Scalars['Int']>;
  id: Scalars['ID'];
  name?: Maybe<Scalars['String']>;
  status?: Maybe<FacilityStatusType>;
  tenants?: Maybe<Array<Tenant>>;
  tenantsCount?: Maybe<Scalars['Int']>;
  updatedAt?: Maybe<Scalars['DateTime']>;
};


export type FacilityDeviceReadAvgArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type FacilityDeviceReadCurrentArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type FacilityDeviceReadSumArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type FacilityDevicesArgs = {
  orderBy?: Array<DeviceOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: DeviceWhereInput;
};


export type FacilityDevicesCountArgs = {
  where?: DeviceWhereInput;
};


export type FacilityTenantsArgs = {
  orderBy?: Array<TenantOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: TenantWhereInput;
};


export type FacilityTenantsCountArgs = {
  where?: TenantWhereInput;
};

export type FacilityCreateInput = {
  devices?: InputMaybe<DeviceRelateToManyForCreateInput>;
  name?: InputMaybe<Scalars['String']>;
  status?: InputMaybe<FacilityStatusType>;
  tenants?: InputMaybe<TenantRelateToManyForCreateInput>;
};

export type FacilityManyRelationFilter = {
  every?: InputMaybe<FacilityWhereInput>;
  none?: InputMaybe<FacilityWhereInput>;
  some?: InputMaybe<FacilityWhereInput>;
};

export type FacilityOrderByInput = {
  createdAt?: InputMaybe<OrderDirection>;
  id?: InputMaybe<OrderDirection>;
  name?: InputMaybe<OrderDirection>;
  status?: InputMaybe<OrderDirection>;
  updatedAt?: InputMaybe<OrderDirection>;
};

export type FacilityRelateToManyForCreateInput = {
  connect?: InputMaybe<Array<FacilityWhereUniqueInput>>;
  create?: InputMaybe<Array<FacilityCreateInput>>;
};

export type FacilityRelateToManyForUpdateInput = {
  connect?: InputMaybe<Array<FacilityWhereUniqueInput>>;
  create?: InputMaybe<Array<FacilityCreateInput>>;
  disconnect?: InputMaybe<Array<FacilityWhereUniqueInput>>;
  set?: InputMaybe<Array<FacilityWhereUniqueInput>>;
};

export type FacilityRelateToOneForCreateInput = {
  connect?: InputMaybe<FacilityWhereUniqueInput>;
  create?: InputMaybe<FacilityCreateInput>;
};

export type FacilityRelateToOneForUpdateInput = {
  connect?: InputMaybe<FacilityWhereUniqueInput>;
  create?: InputMaybe<FacilityCreateInput>;
  disconnect?: InputMaybe<Scalars['Boolean']>;
};

export enum FacilityStatusType {
  Active = 'active',
  Blocked = 'blocked',
  Inactive = 'inactive'
}

export type FacilityStatusTypeNullableFilter = {
  equals?: InputMaybe<FacilityStatusType>;
  in?: InputMaybe<Array<FacilityStatusType>>;
  not?: InputMaybe<FacilityStatusTypeNullableFilter>;
  notIn?: InputMaybe<Array<FacilityStatusType>>;
};

export type FacilityUpdateArgs = {
  data: FacilityUpdateInput;
  where: FacilityWhereUniqueInput;
};

export type FacilityUpdateInput = {
  devices?: InputMaybe<DeviceRelateToManyForUpdateInput>;
  name?: InputMaybe<Scalars['String']>;
  status?: InputMaybe<FacilityStatusType>;
  tenants?: InputMaybe<TenantRelateToManyForUpdateInput>;
};

export type FacilityWhereInput = {
  AND?: InputMaybe<Array<FacilityWhereInput>>;
  NOT?: InputMaybe<Array<FacilityWhereInput>>;
  OR?: InputMaybe<Array<FacilityWhereInput>>;
  createdAt?: InputMaybe<DateTimeNullableFilter>;
  devices?: InputMaybe<DeviceManyRelationFilter>;
  id?: InputMaybe<IdFilter>;
  name?: InputMaybe<StringFilter>;
  status?: InputMaybe<FacilityStatusTypeNullableFilter>;
  tenants?: InputMaybe<TenantManyRelationFilter>;
  updatedAt?: InputMaybe<DateTimeNullableFilter>;
};

export type FacilityWhereUniqueInput = {
  id?: InputMaybe<Scalars['ID']>;
  name?: InputMaybe<Scalars['String']>;
};

export type FloatFilter = {
  equals?: InputMaybe<Scalars['Float']>;
  gt?: InputMaybe<Scalars['Float']>;
  gte?: InputMaybe<Scalars['Float']>;
  in?: InputMaybe<Array<Scalars['Float']>>;
  lt?: InputMaybe<Scalars['Float']>;
  lte?: InputMaybe<Scalars['Float']>;
  not?: InputMaybe<FloatFilter>;
  notIn?: InputMaybe<Array<Scalars['Float']>>;
};

export type IdFilter = {
  equals?: InputMaybe<Scalars['ID']>;
  gt?: InputMaybe<Scalars['ID']>;
  gte?: InputMaybe<Scalars['ID']>;
  in?: InputMaybe<Array<Scalars['ID']>>;
  lt?: InputMaybe<Scalars['ID']>;
  lte?: InputMaybe<Scalars['ID']>;
  not?: InputMaybe<IdFilter>;
  notIn?: InputMaybe<Array<Scalars['ID']>>;
};

export type KeystoneAdminMeta = {
  __typename?: 'KeystoneAdminMeta';
  enableSessionItem: Scalars['Boolean'];
  enableSignout: Scalars['Boolean'];
  list?: Maybe<KeystoneAdminUiListMeta>;
  lists: Array<KeystoneAdminUiListMeta>;
};


export type KeystoneAdminMetaListArgs = {
  key: Scalars['String'];
};

export type KeystoneAdminUiFieldMeta = {
  __typename?: 'KeystoneAdminUIFieldMeta';
  createView: KeystoneAdminUiFieldMetaCreateView;
  customViewsIndex?: Maybe<Scalars['Int']>;
  fieldMeta?: Maybe<Scalars['JSON']>;
  isFilterable: Scalars['Boolean'];
  isOrderable: Scalars['Boolean'];
  itemView?: Maybe<KeystoneAdminUiFieldMetaItemView>;
  label: Scalars['String'];
  listView: KeystoneAdminUiFieldMetaListView;
  path: Scalars['String'];
  search?: Maybe<QueryMode>;
  viewsIndex: Scalars['Int'];
};


export type KeystoneAdminUiFieldMetaItemViewArgs = {
  id?: InputMaybe<Scalars['ID']>;
};

export type KeystoneAdminUiFieldMetaCreateView = {
  __typename?: 'KeystoneAdminUIFieldMetaCreateView';
  fieldMode: KeystoneAdminUiFieldMetaCreateViewFieldMode;
};

export enum KeystoneAdminUiFieldMetaCreateViewFieldMode {
  Edit = 'edit',
  Hidden = 'hidden'
}

export type KeystoneAdminUiFieldMetaItemView = {
  __typename?: 'KeystoneAdminUIFieldMetaItemView';
  fieldMode?: Maybe<KeystoneAdminUiFieldMetaItemViewFieldMode>;
};

export enum KeystoneAdminUiFieldMetaItemViewFieldMode {
  Edit = 'edit',
  Hidden = 'hidden',
  Read = 'read'
}

export type KeystoneAdminUiFieldMetaListView = {
  __typename?: 'KeystoneAdminUIFieldMetaListView';
  fieldMode: KeystoneAdminUiFieldMetaListViewFieldMode;
};

export enum KeystoneAdminUiFieldMetaListViewFieldMode {
  Hidden = 'hidden',
  Read = 'read'
}

export type KeystoneAdminUiListMeta = {
  __typename?: 'KeystoneAdminUIListMeta';
  description?: Maybe<Scalars['String']>;
  fields: Array<KeystoneAdminUiFieldMeta>;
  hideCreate: Scalars['Boolean'];
  hideDelete: Scalars['Boolean'];
  initialColumns: Array<Scalars['String']>;
  initialSort?: Maybe<KeystoneAdminUiSort>;
  isHidden: Scalars['Boolean'];
  itemQueryName: Scalars['String'];
  key: Scalars['String'];
  label: Scalars['String'];
  labelField: Scalars['String'];
  listQueryName: Scalars['String'];
  pageSize: Scalars['Int'];
  path: Scalars['String'];
  plural: Scalars['String'];
  singular: Scalars['String'];
};

export type KeystoneAdminUiSort = {
  __typename?: 'KeystoneAdminUISort';
  direction: KeystoneAdminUiSortDirection;
  field: Scalars['String'];
};

export enum KeystoneAdminUiSortDirection {
  Asc = 'ASC',
  Desc = 'DESC'
}

export type KeystoneMeta = {
  __typename?: 'KeystoneMeta';
  adminMeta: KeystoneAdminMeta;
};

export type Mutation = {
  __typename?: 'Mutation';
  authenticateUserWithPassword?: Maybe<UserAuthenticationWithPasswordResult>;
  createDevice?: Maybe<Device>;
  createDeviceRead?: Maybe<DeviceRead>;
  createDeviceReads?: Maybe<Array<Maybe<DeviceRead>>>;
  createDeviceType?: Maybe<DeviceType>;
  createDeviceTypes?: Maybe<Array<Maybe<DeviceType>>>;
  createDevices?: Maybe<Array<Maybe<Device>>>;
  createFacilities?: Maybe<Array<Maybe<Facility>>>;
  createFacility?: Maybe<Facility>;
  createInitialUser: UserAuthenticationWithPasswordSuccess;
  createResource?: Maybe<Resource>;
  createResources?: Maybe<Array<Maybe<Resource>>>;
  createTenant?: Maybe<Tenant>;
  createTenants?: Maybe<Array<Maybe<Tenant>>>;
  createUser?: Maybe<User>;
  createUsers?: Maybe<Array<Maybe<User>>>;
  deleteDevice?: Maybe<Device>;
  deleteDeviceRead?: Maybe<DeviceRead>;
  deleteDeviceReads?: Maybe<Array<Maybe<DeviceRead>>>;
  deleteDeviceType?: Maybe<DeviceType>;
  deleteDeviceTypes?: Maybe<Array<Maybe<DeviceType>>>;
  deleteDevices?: Maybe<Array<Maybe<Device>>>;
  deleteFacilities?: Maybe<Array<Maybe<Facility>>>;
  deleteFacility?: Maybe<Facility>;
  deleteResource?: Maybe<Resource>;
  deleteResources?: Maybe<Array<Maybe<Resource>>>;
  deleteTenant?: Maybe<Tenant>;
  deleteTenants?: Maybe<Array<Maybe<Tenant>>>;
  deleteUser?: Maybe<User>;
  deleteUsers?: Maybe<Array<Maybe<User>>>;
  endSession: Scalars['Boolean'];
  redeemUserPasswordResetToken?: Maybe<RedeemUserPasswordResetTokenResult>;
  sendUserPasswordResetLink: Scalars['Boolean'];
  updateDevice?: Maybe<Device>;
  updateDeviceRead?: Maybe<DeviceRead>;
  updateDeviceReads?: Maybe<Array<Maybe<DeviceRead>>>;
  updateDeviceType?: Maybe<DeviceType>;
  updateDeviceTypes?: Maybe<Array<Maybe<DeviceType>>>;
  updateDevices?: Maybe<Array<Maybe<Device>>>;
  updateFacilities?: Maybe<Array<Maybe<Facility>>>;
  updateFacility?: Maybe<Facility>;
  updateResource?: Maybe<Resource>;
  updateResources?: Maybe<Array<Maybe<Resource>>>;
  updateTenant?: Maybe<Tenant>;
  updateTenants?: Maybe<Array<Maybe<Tenant>>>;
  updateUser?: Maybe<User>;
  updateUsers?: Maybe<Array<Maybe<User>>>;
};


export type MutationAuthenticateUserWithPasswordArgs = {
  email: Scalars['String'];
  password: Scalars['String'];
};


export type MutationCreateDeviceArgs = {
  data: DeviceCreateInput;
};


export type MutationCreateDeviceReadArgs = {
  data: DeviceReadCreateInput;
};


export type MutationCreateDeviceReadsArgs = {
  data: Array<DeviceReadCreateInput>;
};


export type MutationCreateDeviceTypeArgs = {
  data: DeviceTypeCreateInput;
};


export type MutationCreateDeviceTypesArgs = {
  data: Array<DeviceTypeCreateInput>;
};


export type MutationCreateDevicesArgs = {
  data: Array<DeviceCreateInput>;
};


export type MutationCreateFacilitiesArgs = {
  data: Array<FacilityCreateInput>;
};


export type MutationCreateFacilityArgs = {
  data: FacilityCreateInput;
};


export type MutationCreateInitialUserArgs = {
  data: CreateInitialUserInput;
};


export type MutationCreateResourceArgs = {
  data: ResourceCreateInput;
};


export type MutationCreateResourcesArgs = {
  data: Array<ResourceCreateInput>;
};


export type MutationCreateTenantArgs = {
  data: TenantCreateInput;
};


export type MutationCreateTenantsArgs = {
  data: Array<TenantCreateInput>;
};


export type MutationCreateUserArgs = {
  data: UserCreateInput;
};


export type MutationCreateUsersArgs = {
  data: Array<UserCreateInput>;
};


export type MutationDeleteDeviceArgs = {
  where: DeviceWhereUniqueInput;
};


export type MutationDeleteDeviceReadArgs = {
  where: DeviceReadWhereUniqueInput;
};


export type MutationDeleteDeviceReadsArgs = {
  where: Array<DeviceReadWhereUniqueInput>;
};


export type MutationDeleteDeviceTypeArgs = {
  where: DeviceTypeWhereUniqueInput;
};


export type MutationDeleteDeviceTypesArgs = {
  where: Array<DeviceTypeWhereUniqueInput>;
};


export type MutationDeleteDevicesArgs = {
  where: Array<DeviceWhereUniqueInput>;
};


export type MutationDeleteFacilitiesArgs = {
  where: Array<FacilityWhereUniqueInput>;
};


export type MutationDeleteFacilityArgs = {
  where: FacilityWhereUniqueInput;
};


export type MutationDeleteResourceArgs = {
  where: ResourceWhereUniqueInput;
};


export type MutationDeleteResourcesArgs = {
  where: Array<ResourceWhereUniqueInput>;
};


export type MutationDeleteTenantArgs = {
  where: TenantWhereUniqueInput;
};


export type MutationDeleteTenantsArgs = {
  where: Array<TenantWhereUniqueInput>;
};


export type MutationDeleteUserArgs = {
  where: UserWhereUniqueInput;
};


export type MutationDeleteUsersArgs = {
  where: Array<UserWhereUniqueInput>;
};


export type MutationRedeemUserPasswordResetTokenArgs = {
  email: Scalars['String'];
  password: Scalars['String'];
  token: Scalars['String'];
};


export type MutationSendUserPasswordResetLinkArgs = {
  email: Scalars['String'];
};


export type MutationUpdateDeviceArgs = {
  data: DeviceUpdateInput;
  where: DeviceWhereUniqueInput;
};


export type MutationUpdateDeviceReadArgs = {
  data: DeviceReadUpdateInput;
  where: DeviceReadWhereUniqueInput;
};


export type MutationUpdateDeviceReadsArgs = {
  data: Array<DeviceReadUpdateArgs>;
};


export type MutationUpdateDeviceTypeArgs = {
  data: DeviceTypeUpdateInput;
  where: DeviceTypeWhereUniqueInput;
};


export type MutationUpdateDeviceTypesArgs = {
  data: Array<DeviceTypeUpdateArgs>;
};


export type MutationUpdateDevicesArgs = {
  data: Array<DeviceUpdateArgs>;
};


export type MutationUpdateFacilitiesArgs = {
  data: Array<FacilityUpdateArgs>;
};


export type MutationUpdateFacilityArgs = {
  data: FacilityUpdateInput;
  where: FacilityWhereUniqueInput;
};


export type MutationUpdateResourceArgs = {
  data: ResourceUpdateInput;
  where: ResourceWhereUniqueInput;
};


export type MutationUpdateResourcesArgs = {
  data: Array<ResourceUpdateArgs>;
};


export type MutationUpdateTenantArgs = {
  data: TenantUpdateInput;
  where: TenantWhereUniqueInput;
};


export type MutationUpdateTenantsArgs = {
  data: Array<TenantUpdateArgs>;
};


export type MutationUpdateUserArgs = {
  data: UserUpdateInput;
  where: UserWhereUniqueInput;
};


export type MutationUpdateUsersArgs = {
  data: Array<UserUpdateArgs>;
};

export type NestedStringFilter = {
  contains?: InputMaybe<Scalars['String']>;
  endsWith?: InputMaybe<Scalars['String']>;
  equals?: InputMaybe<Scalars['String']>;
  gt?: InputMaybe<Scalars['String']>;
  gte?: InputMaybe<Scalars['String']>;
  in?: InputMaybe<Array<Scalars['String']>>;
  lt?: InputMaybe<Scalars['String']>;
  lte?: InputMaybe<Scalars['String']>;
  not?: InputMaybe<NestedStringFilter>;
  notIn?: InputMaybe<Array<Scalars['String']>>;
  startsWith?: InputMaybe<Scalars['String']>;
};

export enum OrderDirection {
  Asc = 'asc',
  Desc = 'desc'
}

export type PasswordFilter = {
  isSet: Scalars['Boolean'];
};

export enum PasswordResetRedemptionErrorCode {
  Failure = 'FAILURE',
  TokenExpired = 'TOKEN_EXPIRED',
  TokenRedeemed = 'TOKEN_REDEEMED'
}

export type PasswordState = {
  __typename?: 'PasswordState';
  isSet: Scalars['Boolean'];
};

export type Query = {
  __typename?: 'Query';
  authenticatedItem?: Maybe<AuthenticatedItem>;
  device?: Maybe<Device>;
  deviceRead?: Maybe<DeviceRead>;
  deviceReads?: Maybe<Array<DeviceRead>>;
  deviceReadsCount?: Maybe<Scalars['Int']>;
  deviceType?: Maybe<DeviceType>;
  deviceTypes?: Maybe<Array<DeviceType>>;
  deviceTypesCount?: Maybe<Scalars['Int']>;
  devices?: Maybe<Array<Device>>;
  devicesCount?: Maybe<Scalars['Int']>;
  facilities?: Maybe<Array<Facility>>;
  facilitiesCount?: Maybe<Scalars['Int']>;
  facility?: Maybe<Facility>;
  keystone: KeystoneMeta;
  resource?: Maybe<Resource>;
  resources?: Maybe<Array<Resource>>;
  resourcesCount?: Maybe<Scalars['Int']>;
  tenant?: Maybe<Tenant>;
  tenants?: Maybe<Array<Tenant>>;
  tenantsCount?: Maybe<Scalars['Int']>;
  user?: Maybe<User>;
  users?: Maybe<Array<User>>;
  usersCount?: Maybe<Scalars['Int']>;
  validateUserPasswordResetToken?: Maybe<ValidateUserPasswordResetTokenResult>;
};


export type QueryDeviceArgs = {
  where: DeviceWhereUniqueInput;
};


export type QueryDeviceReadArgs = {
  where: DeviceReadWhereUniqueInput;
};


export type QueryDeviceReadsArgs = {
  orderBy?: Array<DeviceReadOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: DeviceReadWhereInput;
};


export type QueryDeviceReadsCountArgs = {
  where?: DeviceReadWhereInput;
};


export type QueryDeviceTypeArgs = {
  where: DeviceTypeWhereUniqueInput;
};


export type QueryDeviceTypesArgs = {
  orderBy?: Array<DeviceTypeOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: DeviceTypeWhereInput;
};


export type QueryDeviceTypesCountArgs = {
  where?: DeviceTypeWhereInput;
};


export type QueryDevicesArgs = {
  orderBy?: Array<DeviceOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: DeviceWhereInput;
};


export type QueryDevicesCountArgs = {
  where?: DeviceWhereInput;
};


export type QueryFacilitiesArgs = {
  orderBy?: Array<FacilityOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: FacilityWhereInput;
};


export type QueryFacilitiesCountArgs = {
  where?: FacilityWhereInput;
};


export type QueryFacilityArgs = {
  where: FacilityWhereUniqueInput;
};


export type QueryResourceArgs = {
  where: ResourceWhereUniqueInput;
};


export type QueryResourcesArgs = {
  orderBy?: Array<ResourceOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: ResourceWhereInput;
};


export type QueryResourcesCountArgs = {
  where?: ResourceWhereInput;
};


export type QueryTenantArgs = {
  where: TenantWhereUniqueInput;
};


export type QueryTenantsArgs = {
  orderBy?: Array<TenantOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: TenantWhereInput;
};


export type QueryTenantsCountArgs = {
  where?: TenantWhereInput;
};


export type QueryUserArgs = {
  where: UserWhereUniqueInput;
};


export type QueryUsersArgs = {
  orderBy?: Array<UserOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: UserWhereInput;
};


export type QueryUsersCountArgs = {
  where?: UserWhereInput;
};


export type QueryValidateUserPasswordResetTokenArgs = {
  email: Scalars['String'];
  token: Scalars['String'];
};

export enum QueryMode {
  Default = 'default',
  Insensitive = 'insensitive'
}

export type RedeemUserPasswordResetTokenResult = {
  __typename?: 'RedeemUserPasswordResetTokenResult';
  code: PasswordResetRedemptionErrorCode;
  message: Scalars['String'];
};

export type Resource = {
  __typename?: 'Resource';
  capacity?: Maybe<Scalars['Float']>;
  createdAt?: Maybe<Scalars['DateTime']>;
  deviceReadAvg?: Maybe<Scalars['Float']>;
  deviceReadCurrent?: Maybe<Scalars['Float']>;
  deviceReadSum?: Maybe<Scalars['Float']>;
  devices?: Maybe<Array<Device>>;
  devicesCount?: Maybe<Scalars['Int']>;
  id: Scalars['ID'];
  name?: Maybe<Scalars['String']>;
  resourceCategory?: Maybe<ResourceResourceCategoryType>;
  status?: Maybe<ResourceStatusType>;
  tenant?: Maybe<Tenant>;
  unit?: Maybe<ResourceUnitType>;
  updatedAt?: Maybe<Scalars['DateTime']>;
};


export type ResourceDeviceReadAvgArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type ResourceDeviceReadCurrentArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type ResourceDeviceReadSumArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type ResourceDevicesArgs = {
  orderBy?: Array<DeviceOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: DeviceWhereInput;
};


export type ResourceDevicesCountArgs = {
  where?: DeviceWhereInput;
};

export type ResourceCreateInput = {
  capacity?: InputMaybe<Scalars['Float']>;
  devices?: InputMaybe<DeviceRelateToManyForCreateInput>;
  name?: InputMaybe<Scalars['String']>;
  resourceCategory?: InputMaybe<ResourceResourceCategoryType>;
  status?: InputMaybe<ResourceStatusType>;
  tenant?: InputMaybe<TenantRelateToOneForCreateInput>;
  unit?: InputMaybe<ResourceUnitType>;
};

export type ResourceManyRelationFilter = {
  every?: InputMaybe<ResourceWhereInput>;
  none?: InputMaybe<ResourceWhereInput>;
  some?: InputMaybe<ResourceWhereInput>;
};

export type ResourceOrderByInput = {
  capacity?: InputMaybe<OrderDirection>;
  createdAt?: InputMaybe<OrderDirection>;
  id?: InputMaybe<OrderDirection>;
  name?: InputMaybe<OrderDirection>;
  resourceCategory?: InputMaybe<OrderDirection>;
  status?: InputMaybe<OrderDirection>;
  unit?: InputMaybe<OrderDirection>;
  updatedAt?: InputMaybe<OrderDirection>;
};

export type ResourceRelateToManyForCreateInput = {
  connect?: InputMaybe<Array<ResourceWhereUniqueInput>>;
  create?: InputMaybe<Array<ResourceCreateInput>>;
};

export type ResourceRelateToManyForUpdateInput = {
  connect?: InputMaybe<Array<ResourceWhereUniqueInput>>;
  create?: InputMaybe<Array<ResourceCreateInput>>;
  disconnect?: InputMaybe<Array<ResourceWhereUniqueInput>>;
  set?: InputMaybe<Array<ResourceWhereUniqueInput>>;
};

export type ResourceRelateToOneForCreateInput = {
  connect?: InputMaybe<ResourceWhereUniqueInput>;
  create?: InputMaybe<ResourceCreateInput>;
};

export type ResourceRelateToOneForUpdateInput = {
  connect?: InputMaybe<ResourceWhereUniqueInput>;
  create?: InputMaybe<ResourceCreateInput>;
  disconnect?: InputMaybe<Scalars['Boolean']>;
};

export enum ResourceResourceCategoryType {
  Power = 'power',
  SewageTreatment = 'sewage_treatment',
  Water = 'water'
}

export type ResourceResourceCategoryTypeNullableFilter = {
  equals?: InputMaybe<ResourceResourceCategoryType>;
  in?: InputMaybe<Array<ResourceResourceCategoryType>>;
  not?: InputMaybe<ResourceResourceCategoryTypeNullableFilter>;
  notIn?: InputMaybe<Array<ResourceResourceCategoryType>>;
};

export enum ResourceStatusType {
  Active = 'active',
  Blocked = 'blocked',
  Inactive = 'inactive'
}

export type ResourceStatusTypeNullableFilter = {
  equals?: InputMaybe<ResourceStatusType>;
  in?: InputMaybe<Array<ResourceStatusType>>;
  not?: InputMaybe<ResourceStatusTypeNullableFilter>;
  notIn?: InputMaybe<Array<ResourceStatusType>>;
};

export enum ResourceUnitType {
  Kw = 'kw',
  Ltr = 'ltr'
}

export type ResourceUnitTypeNullableFilter = {
  equals?: InputMaybe<ResourceUnitType>;
  in?: InputMaybe<Array<ResourceUnitType>>;
  not?: InputMaybe<ResourceUnitTypeNullableFilter>;
  notIn?: InputMaybe<Array<ResourceUnitType>>;
};

export type ResourceUpdateArgs = {
  data: ResourceUpdateInput;
  where: ResourceWhereUniqueInput;
};

export type ResourceUpdateInput = {
  capacity?: InputMaybe<Scalars['Float']>;
  devices?: InputMaybe<DeviceRelateToManyForUpdateInput>;
  name?: InputMaybe<Scalars['String']>;
  resourceCategory?: InputMaybe<ResourceResourceCategoryType>;
  status?: InputMaybe<ResourceStatusType>;
  tenant?: InputMaybe<TenantRelateToOneForUpdateInput>;
  unit?: InputMaybe<ResourceUnitType>;
};

export type ResourceWhereInput = {
  AND?: InputMaybe<Array<ResourceWhereInput>>;
  NOT?: InputMaybe<Array<ResourceWhereInput>>;
  OR?: InputMaybe<Array<ResourceWhereInput>>;
  capacity?: InputMaybe<FloatFilter>;
  createdAt?: InputMaybe<DateTimeNullableFilter>;
  devices?: InputMaybe<DeviceManyRelationFilter>;
  id?: InputMaybe<IdFilter>;
  name?: InputMaybe<StringFilter>;
  resourceCategory?: InputMaybe<ResourceResourceCategoryTypeNullableFilter>;
  status?: InputMaybe<ResourceStatusTypeNullableFilter>;
  tenant?: InputMaybe<TenantWhereInput>;
  unit?: InputMaybe<ResourceUnitTypeNullableFilter>;
  updatedAt?: InputMaybe<DateTimeNullableFilter>;
};

export type ResourceWhereUniqueInput = {
  id?: InputMaybe<Scalars['ID']>;
  name?: InputMaybe<Scalars['String']>;
};

export type StringFilter = {
  contains?: InputMaybe<Scalars['String']>;
  endsWith?: InputMaybe<Scalars['String']>;
  equals?: InputMaybe<Scalars['String']>;
  gt?: InputMaybe<Scalars['String']>;
  gte?: InputMaybe<Scalars['String']>;
  in?: InputMaybe<Array<Scalars['String']>>;
  lt?: InputMaybe<Scalars['String']>;
  lte?: InputMaybe<Scalars['String']>;
  mode?: InputMaybe<QueryMode>;
  not?: InputMaybe<NestedStringFilter>;
  notIn?: InputMaybe<Array<Scalars['String']>>;
  startsWith?: InputMaybe<Scalars['String']>;
};

export type Tenant = {
  __typename?: 'Tenant';
  children?: Maybe<Array<Tenant>>;
  childrenCount?: Maybe<Scalars['Int']>;
  createdAt?: Maybe<Scalars['DateTime']>;
  description?: Maybe<Scalars['String']>;
  deviceReadAvg?: Maybe<Scalars['Float']>;
  deviceReadCurrent?: Maybe<Scalars['Float']>;
  deviceReadSum?: Maybe<Scalars['Float']>;
  devices?: Maybe<Array<Device>>;
  devicesCount?: Maybe<Scalars['Int']>;
  facilities?: Maybe<Array<Facility>>;
  facilitiesCount?: Maybe<Scalars['Int']>;
  id: Scalars['ID'];
  location?: Maybe<Scalars['String']>;
  name?: Maybe<Scalars['String']>;
  owners?: Maybe<Array<User>>;
  ownersCount?: Maybe<Scalars['Int']>;
  parent?: Maybe<Tenant>;
  parents?: Maybe<Array<User>>;
  parentsCount?: Maybe<Scalars['Int']>;
  resources?: Maybe<Array<Resource>>;
  resourcesCount?: Maybe<Scalars['Int']>;
  status?: Maybe<TenantStatusType>;
  updatedAt?: Maybe<Scalars['DateTime']>;
};


export type TenantChildrenArgs = {
  orderBy?: Array<TenantOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: TenantWhereInput;
};


export type TenantChildrenCountArgs = {
  where?: TenantWhereInput;
};


export type TenantDeviceReadAvgArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type TenantDeviceReadCurrentArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type TenantDeviceReadSumArgs = {
  from?: Scalars['DateTime'];
  to?: Scalars['DateTime'];
};


export type TenantDevicesArgs = {
  orderBy?: Array<DeviceOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: DeviceWhereInput;
};


export type TenantDevicesCountArgs = {
  where?: DeviceWhereInput;
};


export type TenantFacilitiesArgs = {
  orderBy?: Array<FacilityOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: FacilityWhereInput;
};


export type TenantFacilitiesCountArgs = {
  where?: FacilityWhereInput;
};


export type TenantOwnersArgs = {
  orderBy?: Array<UserOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: UserWhereInput;
};


export type TenantOwnersCountArgs = {
  where?: UserWhereInput;
};


export type TenantParentsArgs = {
  orderBy?: Array<UserOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: UserWhereInput;
};


export type TenantParentsCountArgs = {
  where?: UserWhereInput;
};


export type TenantResourcesArgs = {
  orderBy?: Array<ResourceOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: ResourceWhereInput;
};


export type TenantResourcesCountArgs = {
  where?: ResourceWhereInput;
};

export type TenantCreateInput = {
  children?: InputMaybe<TenantRelateToManyForCreateInput>;
  description?: InputMaybe<Scalars['String']>;
  devices?: InputMaybe<DeviceRelateToManyForCreateInput>;
  facilities?: InputMaybe<FacilityRelateToManyForCreateInput>;
  location?: InputMaybe<Scalars['String']>;
  name?: InputMaybe<Scalars['String']>;
  owners?: InputMaybe<UserRelateToManyForCreateInput>;
  parent?: InputMaybe<TenantRelateToOneForCreateInput>;
  parents?: InputMaybe<UserRelateToManyForCreateInput>;
  resources?: InputMaybe<ResourceRelateToManyForCreateInput>;
  status?: InputMaybe<TenantStatusType>;
};

export type TenantManyRelationFilter = {
  every?: InputMaybe<TenantWhereInput>;
  none?: InputMaybe<TenantWhereInput>;
  some?: InputMaybe<TenantWhereInput>;
};

export type TenantOrderByInput = {
  createdAt?: InputMaybe<OrderDirection>;
  description?: InputMaybe<OrderDirection>;
  id?: InputMaybe<OrderDirection>;
  location?: InputMaybe<OrderDirection>;
  name?: InputMaybe<OrderDirection>;
  status?: InputMaybe<OrderDirection>;
  updatedAt?: InputMaybe<OrderDirection>;
};

export type TenantRelateToManyForCreateInput = {
  connect?: InputMaybe<Array<TenantWhereUniqueInput>>;
  create?: InputMaybe<Array<TenantCreateInput>>;
};

export type TenantRelateToManyForUpdateInput = {
  connect?: InputMaybe<Array<TenantWhereUniqueInput>>;
  create?: InputMaybe<Array<TenantCreateInput>>;
  disconnect?: InputMaybe<Array<TenantWhereUniqueInput>>;
  set?: InputMaybe<Array<TenantWhereUniqueInput>>;
};

export type TenantRelateToOneForCreateInput = {
  connect?: InputMaybe<TenantWhereUniqueInput>;
  create?: InputMaybe<TenantCreateInput>;
};

export type TenantRelateToOneForUpdateInput = {
  connect?: InputMaybe<TenantWhereUniqueInput>;
  create?: InputMaybe<TenantCreateInput>;
  disconnect?: InputMaybe<Scalars['Boolean']>;
};

export enum TenantStatusType {
  Active = 'active',
  Blocked = 'blocked',
  Inactive = 'inactive'
}

export type TenantStatusTypeNullableFilter = {
  equals?: InputMaybe<TenantStatusType>;
  in?: InputMaybe<Array<TenantStatusType>>;
  not?: InputMaybe<TenantStatusTypeNullableFilter>;
  notIn?: InputMaybe<Array<TenantStatusType>>;
};

export type TenantUpdateArgs = {
  data: TenantUpdateInput;
  where: TenantWhereUniqueInput;
};

export type TenantUpdateInput = {
  children?: InputMaybe<TenantRelateToManyForUpdateInput>;
  description?: InputMaybe<Scalars['String']>;
  devices?: InputMaybe<DeviceRelateToManyForUpdateInput>;
  facilities?: InputMaybe<FacilityRelateToManyForUpdateInput>;
  location?: InputMaybe<Scalars['String']>;
  name?: InputMaybe<Scalars['String']>;
  owners?: InputMaybe<UserRelateToManyForUpdateInput>;
  parent?: InputMaybe<TenantRelateToOneForUpdateInput>;
  parents?: InputMaybe<UserRelateToManyForUpdateInput>;
  resources?: InputMaybe<ResourceRelateToManyForUpdateInput>;
  status?: InputMaybe<TenantStatusType>;
};

export type TenantWhereInput = {
  AND?: InputMaybe<Array<TenantWhereInput>>;
  NOT?: InputMaybe<Array<TenantWhereInput>>;
  OR?: InputMaybe<Array<TenantWhereInput>>;
  children?: InputMaybe<TenantManyRelationFilter>;
  createdAt?: InputMaybe<DateTimeNullableFilter>;
  description?: InputMaybe<StringFilter>;
  devices?: InputMaybe<DeviceManyRelationFilter>;
  facilities?: InputMaybe<FacilityManyRelationFilter>;
  id?: InputMaybe<IdFilter>;
  location?: InputMaybe<StringFilter>;
  name?: InputMaybe<StringFilter>;
  owners?: InputMaybe<UserManyRelationFilter>;
  parent?: InputMaybe<TenantWhereInput>;
  parents?: InputMaybe<UserManyRelationFilter>;
  resources?: InputMaybe<ResourceManyRelationFilter>;
  status?: InputMaybe<TenantStatusTypeNullableFilter>;
  updatedAt?: InputMaybe<DateTimeNullableFilter>;
};

export type TenantWhereUniqueInput = {
  id?: InputMaybe<Scalars['ID']>;
};

export type User = {
  __typename?: 'User';
  createdAt?: Maybe<Scalars['DateTime']>;
  email?: Maybe<Scalars['String']>;
  id: Scalars['ID'];
  name?: Maybe<Scalars['String']>;
  password?: Maybe<PasswordState>;
  passwordResetIssuedAt?: Maybe<Scalars['DateTime']>;
  passwordResetRedeemedAt?: Maybe<Scalars['DateTime']>;
  passwordResetToken?: Maybe<PasswordState>;
  phone?: Maybe<Scalars['String']>;
  role?: Maybe<UserRoleType>;
  status?: Maybe<UserStatusType>;
  subTenants?: Maybe<Array<Tenant>>;
  subTenantsCount?: Maybe<Scalars['Int']>;
  tenant?: Maybe<Tenant>;
  updatedAt?: Maybe<Scalars['DateTime']>;
};


export type UserSubTenantsArgs = {
  orderBy?: Array<TenantOrderByInput>;
  skip?: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  where?: TenantWhereInput;
};


export type UserSubTenantsCountArgs = {
  where?: TenantWhereInput;
};

export type UserAuthenticationWithPasswordFailure = {
  __typename?: 'UserAuthenticationWithPasswordFailure';
  message: Scalars['String'];
};

export type UserAuthenticationWithPasswordResult = UserAuthenticationWithPasswordFailure | UserAuthenticationWithPasswordSuccess;

export type UserAuthenticationWithPasswordSuccess = {
  __typename?: 'UserAuthenticationWithPasswordSuccess';
  item: User;
  sessionToken: Scalars['String'];
};

export type UserCreateInput = {
  email?: InputMaybe<Scalars['String']>;
  name?: InputMaybe<Scalars['String']>;
  password?: InputMaybe<Scalars['String']>;
  passwordResetIssuedAt?: InputMaybe<Scalars['DateTime']>;
  passwordResetRedeemedAt?: InputMaybe<Scalars['DateTime']>;
  passwordResetToken?: InputMaybe<Scalars['String']>;
  phone?: InputMaybe<Scalars['String']>;
  role?: InputMaybe<UserRoleType>;
  status?: InputMaybe<UserStatusType>;
  subTenants?: InputMaybe<TenantRelateToManyForCreateInput>;
  tenant?: InputMaybe<TenantRelateToOneForCreateInput>;
};

export type UserManyRelationFilter = {
  every?: InputMaybe<UserWhereInput>;
  none?: InputMaybe<UserWhereInput>;
  some?: InputMaybe<UserWhereInput>;
};

export type UserOrderByInput = {
  createdAt?: InputMaybe<OrderDirection>;
  email?: InputMaybe<OrderDirection>;
  id?: InputMaybe<OrderDirection>;
  name?: InputMaybe<OrderDirection>;
  passwordResetIssuedAt?: InputMaybe<OrderDirection>;
  passwordResetRedeemedAt?: InputMaybe<OrderDirection>;
  phone?: InputMaybe<OrderDirection>;
  role?: InputMaybe<OrderDirection>;
  status?: InputMaybe<OrderDirection>;
  updatedAt?: InputMaybe<OrderDirection>;
};

export type UserRelateToManyForCreateInput = {
  connect?: InputMaybe<Array<UserWhereUniqueInput>>;
  create?: InputMaybe<Array<UserCreateInput>>;
};

export type UserRelateToManyForUpdateInput = {
  connect?: InputMaybe<Array<UserWhereUniqueInput>>;
  create?: InputMaybe<Array<UserCreateInput>>;
  disconnect?: InputMaybe<Array<UserWhereUniqueInput>>;
  set?: InputMaybe<Array<UserWhereUniqueInput>>;
};

export enum UserRoleType {
  Admin = 'admin',
  Tenant = 'tenant',
  User = 'user'
}

export type UserRoleTypeNullableFilter = {
  equals?: InputMaybe<UserRoleType>;
  in?: InputMaybe<Array<UserRoleType>>;
  not?: InputMaybe<UserRoleTypeNullableFilter>;
  notIn?: InputMaybe<Array<UserRoleType>>;
};

export enum UserStatusType {
  Active = 'active',
  Blocked = 'blocked',
  Inactive = 'inactive'
}

export type UserStatusTypeNullableFilter = {
  equals?: InputMaybe<UserStatusType>;
  in?: InputMaybe<Array<UserStatusType>>;
  not?: InputMaybe<UserStatusTypeNullableFilter>;
  notIn?: InputMaybe<Array<UserStatusType>>;
};

export type UserUpdateArgs = {
  data: UserUpdateInput;
  where: UserWhereUniqueInput;
};

export type UserUpdateInput = {
  email?: InputMaybe<Scalars['String']>;
  name?: InputMaybe<Scalars['String']>;
  password?: InputMaybe<Scalars['String']>;
  passwordResetIssuedAt?: InputMaybe<Scalars['DateTime']>;
  passwordResetRedeemedAt?: InputMaybe<Scalars['DateTime']>;
  passwordResetToken?: InputMaybe<Scalars['String']>;
  phone?: InputMaybe<Scalars['String']>;
  role?: InputMaybe<UserRoleType>;
  status?: InputMaybe<UserStatusType>;
  subTenants?: InputMaybe<TenantRelateToManyForUpdateInput>;
  tenant?: InputMaybe<TenantRelateToOneForUpdateInput>;
};

export type UserWhereInput = {
  AND?: InputMaybe<Array<UserWhereInput>>;
  NOT?: InputMaybe<Array<UserWhereInput>>;
  OR?: InputMaybe<Array<UserWhereInput>>;
  createdAt?: InputMaybe<DateTimeNullableFilter>;
  email?: InputMaybe<StringFilter>;
  id?: InputMaybe<IdFilter>;
  name?: InputMaybe<StringFilter>;
  passwordResetIssuedAt?: InputMaybe<DateTimeNullableFilter>;
  passwordResetRedeemedAt?: InputMaybe<DateTimeNullableFilter>;
  passwordResetToken?: InputMaybe<PasswordFilter>;
  phone?: InputMaybe<StringFilter>;
  role?: InputMaybe<UserRoleTypeNullableFilter>;
  status?: InputMaybe<UserStatusTypeNullableFilter>;
  subTenants?: InputMaybe<TenantManyRelationFilter>;
  tenant?: InputMaybe<TenantWhereInput>;
  updatedAt?: InputMaybe<DateTimeNullableFilter>;
};

export type UserWhereUniqueInput = {
  email?: InputMaybe<Scalars['String']>;
  id?: InputMaybe<Scalars['ID']>;
};

export type ValidateUserPasswordResetTokenResult = {
  __typename?: 'ValidateUserPasswordResetTokenResult';
  code: PasswordResetRedemptionErrorCode;
  message: Scalars['String'];
};

export type AuthenticateUserWithPasswordMutationVariables = Exact<{
  email: Scalars['String'];
  password: Scalars['String'];
}>;


export type AuthenticateUserWithPasswordMutation = { __typename?: 'Mutation', authenticateUserWithPassword?: { __typename?: 'UserAuthenticationWithPasswordFailure', message: string } | { __typename?: 'UserAuthenticationWithPasswordSuccess', sessionToken: string, item: { __typename?: 'User', name?: string | null, email?: string | null, id: string, role?: UserRoleType | null, tenant?: { __typename?: 'Tenant', id: string, name?: string | null, status?: TenantStatusType | null } | null } } | null };

export type SendUserPasswordResetLinkMutationVariables = Exact<{
  email: Scalars['String'];
}>;


export type SendUserPasswordResetLinkMutation = { __typename?: 'Mutation', sendUserPasswordResetLink: boolean };

export type AuthenticatedItemQueryVariables = Exact<{ [key: string]: never; }>;


export type AuthenticatedItemQuery = { __typename?: 'Query', authenticatedItem?: { __typename?: 'User', id: string, name?: string | null, email?: string | null, role?: UserRoleType | null, status?: UserStatusType | null, tenant?: { __typename?: 'Tenant', id: string, name?: string | null, status?: TenantStatusType | null } | null } | null };

export type UsersQueryVariables = Exact<{
  where: UserWhereInput;
  skip: Scalars['Int'];
  take?: InputMaybe<Scalars['Int']>;
  orderBy: Array<UserOrderByInput> | UserOrderByInput;
  usersCountWhere2: UserWhereInput;
}>;


export type UsersQuery = { __typename?: 'Query', usersCount?: number | null, users?: Array<{ __typename?: 'User', id: string, name?: string | null, email?: string | null, role?: UserRoleType | null, phone?: string | null, status?: UserStatusType | null, tenant?: { __typename?: 'Tenant', id: string, name?: string | null } | null }> | null };

export type TenantsQueryVariables = Exact<{
  where: TenantWhereInput;
  orderBy: Array<TenantOrderByInput> | TenantOrderByInput;
  take?: InputMaybe<Scalars['Int']>;
  skip: Scalars['Int'];
  tenantsCountWhere2: TenantWhereInput;
}>;


export type TenantsQuery = { __typename?: 'Query', tenantsCount?: number | null, tenants?: Array<{ __typename?: 'Tenant', id: string, name?: string | null, status?: TenantStatusType | null, location?: string | null, description?: string | null, facilitiesCount?: number | null, owners?: Array<{ __typename?: 'User', id: string, name?: string | null }> | null, facilities?: Array<{ __typename?: 'Facility', id: string, name?: string | null }> | null, parent?: { __typename?: 'Tenant', id: string, name?: string | null } | null, resources?: Array<{ __typename?: 'Resource', id: string, name?: string | null, deviceReadSum?: number | null, resourceCategory?: ResourceResourceCategoryType | null }> | null }> | null };

export type CreateUserMutationVariables = Exact<{
  data: UserCreateInput;
}>;


export type CreateUserMutation = { __typename?: 'Mutation', createUser?: { __typename?: 'User', id: string, name?: string | null, email?: string | null, phone?: string | null, status?: UserStatusType | null } | null };

export type UpdateUserMutationVariables = Exact<{
  where: UserWhereUniqueInput;
  data: UserUpdateInput;
}>;


export type UpdateUserMutation = { __typename?: 'Mutation', updateUser?: { __typename?: 'User', id: string, name?: string | null, email?: string | null, phone?: string | null, role?: UserRoleType | null, status?: UserStatusType | null } | null };

export type LogoutMutationVariables = Exact<{ [key: string]: never; }>;


export type LogoutMutation = { __typename?: 'Mutation', endSession: boolean };

export type CreateTenantMutationVariables = Exact<{
  data: TenantCreateInput;
}>;


export type CreateTenantMutation = { __typename?: 'Mutation', createTenant?: { __typename?: 'Tenant', id: string, name?: string | null, location?: string | null, description?: string | null, status?: TenantStatusType | null, owners?: Array<{ __typename?: 'User', id: string, name?: string | null }> | null } | null };

export type UpdateTenantMutationVariables = Exact<{
  where: TenantWhereUniqueInput;
  data: TenantUpdateInput;
}>;


export type UpdateTenantMutation = { __typename?: 'Mutation', updateTenant?: { __typename?: 'Tenant', id: string, name?: string | null, location?: string | null, description?: string | null, status?: TenantStatusType | null } | null };

export type FacilitiesQueryVariables = Exact<{ [key: string]: never; }>;


export type FacilitiesQuery = { __typename?: 'Query', facilities?: Array<{ __typename?: 'Facility', id: string, name?: string | null }> | null };

export type CreateFacilityMutationVariables = Exact<{
  data: FacilityCreateInput;
}>;


export type CreateFacilityMutation = { __typename?: 'Mutation', createFacility?: { __typename?: 'Facility', id: string, name?: string | null, status?: FacilityStatusType | null } | null };

export type RedeemUserPasswordResetTokenMutationVariables = Exact<{
  email: Scalars['String'];
  token: Scalars['String'];
  password: Scalars['String'];
}>;


export type RedeemUserPasswordResetTokenMutation = { __typename?: 'Mutation', redeemUserPasswordResetToken?: { __typename?: 'RedeemUserPasswordResetTokenResult', code: PasswordResetRedemptionErrorCode, message: string } | null };

export type TenantDetailsQueryVariables = Exact<{
  where: TenantWhereUniqueInput;
}>;


export type TenantDetailsQuery = { __typename?: 'Query', tenant?: { __typename?: 'Tenant', id: string, name?: string | null, location?: string | null, description?: string | null, status?: TenantStatusType | null, resourcesCount?: number | null, childrenCount?: number | null, owners?: Array<{ __typename?: 'User', id: string, name?: string | null }> | null, facilities?: Array<{ __typename?: 'Facility', id: string, name?: string | null }> | null, resources?: Array<{ __typename?: 'Resource', id: string, name?: string | null, resourceCategory?: ResourceResourceCategoryType | null, capacity?: number | null, unit?: ResourceUnitType | null, deviceReadSum?: number | null, deviceReadAvg?: number | null }> | null, children?: Array<{ __typename?: 'Tenant', id: string, name?: string | null, location?: string | null, description?: string | null, status?: TenantStatusType | null, owners?: Array<{ __typename?: 'User', id: string, name?: string | null }> | null, facilities?: Array<{ __typename?: 'Facility', id: string, name?: string | null }> | null }> | null } | null };

export type DevicesQueryVariables = Exact<{
  take?: InputMaybe<Scalars['Int']>;
  skip: Scalars['Int'];
  where: DeviceWhereInput;
  devicesCountWhere2: DeviceWhereInput;
}>;


export type DevicesQuery = { __typename?: 'Query', devicesCount?: number | null, devices?: Array<{ __typename?: 'Device', id: string, name?: string | null, deviceId?: string | null, edgeDeviceId?: string | null, portNumber?: string | null, description?: string | null, status?: DeviceStatusType | null, deviceType?: { __typename?: 'DeviceType', id: string, name?: string | null } | null, facility?: { __typename?: 'Facility', id: string, name?: string | null } | null, resource?: { __typename?: 'Resource', id: string, name?: string | null, resourceCategory?: ResourceResourceCategoryType | null } | null }> | null };

export type CreateDeviceMutationVariables = Exact<{
  data: DeviceCreateInput;
}>;


export type CreateDeviceMutation = { __typename?: 'Mutation', createDevice?: { __typename?: 'Device', id: string, deviceId?: string | null } | null };

export type UpdateDeviceMutationVariables = Exact<{
  where: DeviceWhereUniqueInput;
  data: DeviceUpdateInput;
}>;


export type UpdateDeviceMutation = { __typename?: 'Mutation', updateDevice?: { __typename?: 'Device', id: string, deviceId?: string | null } | null };

export type ResourcesQueryVariables = Exact<{
  where: ResourceWhereInput;
  take?: InputMaybe<Scalars['Int']>;
  skip: Scalars['Int'];
  resourcesCountWhere2: ResourceWhereInput;
}>;


export type ResourcesQuery = { __typename?: 'Query', resourcesCount?: number | null, resources?: Array<{ __typename?: 'Resource', id: string, name?: string | null, resourceCategory?: ResourceResourceCategoryType | null, capacity?: number | null, unit?: ResourceUnitType | null, status?: ResourceStatusType | null }> | null };

export type DeviceTypesQueryVariables = Exact<{ [key: string]: never; }>;


export type DeviceTypesQuery = { __typename?: 'Query', deviceTypes?: Array<{ __typename?: 'DeviceType', id: string, name?: string | null }> | null };

export type FacilitiesUnderTenantQueryVariables = Exact<{
  where: FacilityWhereInput;
}>;


export type FacilitiesUnderTenantQuery = { __typename?: 'Query', facilities?: Array<{ __typename?: 'Facility', id: string, name?: string | null }> | null };

export type CreateResourceMutationVariables = Exact<{
  data: ResourceCreateInput;
}>;


export type CreateResourceMutation = { __typename?: 'Mutation', createResource?: { __typename?: 'Resource', id: string, name?: string | null, status?: ResourceStatusType | null, resourceCategory?: ResourceResourceCategoryType | null } | null };

export type UpdateResourceMutationVariables = Exact<{
  where: ResourceWhereUniqueInput;
  data: ResourceUpdateInput;
}>;


export type UpdateResourceMutation = { __typename?: 'Mutation', updateResource?: { __typename?: 'Resource', id: string, name?: string | null, status?: ResourceStatusType | null, resourceCategory?: ResourceResourceCategoryType | null } | null };

export type ResourcesDataByDateQueryVariables = Exact<{
  from: Scalars['DateTime'];
  to: Scalars['DateTime'];
  where: ResourceWhereInput;
}>;


export type ResourcesDataByDateQuery = { __typename?: 'Query', resources?: Array<{ __typename?: 'Resource', id: string, name?: string | null, status?: ResourceStatusType | null, capacity?: number | null, unit?: ResourceUnitType | null, resourceCategory?: ResourceResourceCategoryType | null, deviceReadSum?: number | null, deviceReadAvg?: number | null, deviceReadCurrent?: number | null }> | null };

export type TenantDetailsByDateQueryVariables = Exact<{
  where: TenantWhereUniqueInput;
  from: Scalars['DateTime'];
  to: Scalars['DateTime'];
  deviceReadSumFrom2: Scalars['DateTime'];
  deviceReadSumTo2: Scalars['DateTime'];
}>;


export type TenantDetailsByDateQuery = { __typename?: 'Query', tenant?: { __typename?: 'Tenant', id: string, name?: string | null, facilities?: Array<{ __typename?: 'Facility', id: string, name?: string | null, deviceReadSum?: number | null, deviceReadAvg?: number | null }> | null, resources?: Array<{ __typename?: 'Resource', id: string, name?: string | null, status?: ResourceStatusType | null, capacity?: number | null, unit?: ResourceUnitType | null, resourceCategory?: ResourceResourceCategoryType | null, deviceReadSum?: number | null, deviceReadAvg?: number | null, deviceReadCurrent?: number | null }> | null } | null };

export type TenantsByDateQueryVariables = Exact<{
  where: TenantWhereInput;
  from: Scalars['DateTime'];
  to: Scalars['DateTime'];
  deviceReadSumFrom2: Scalars['DateTime'];
  deviceReadSumTo2: Scalars['DateTime'];
}>;


export type TenantsByDateQuery = { __typename?: 'Query', tenants?: Array<{ __typename?: 'Tenant', id: string, name?: string | null, facilities?: Array<{ __typename?: 'Facility', id: string, name?: string | null, deviceReadSum?: number | null, deviceReadAvg?: number | null }> | null, resources?: Array<{ __typename?: 'Resource', id: string, name?: string | null, deviceReadSum?: number | null, deviceReadAvg?: number | null, capacity?: number | null, unit?: ResourceUnitType | null }> | null }> | null };

export type TenantsDataByCategoryQueryVariables = Exact<{
  where: ResourceWhereInput;
  from: Scalars['DateTime'];
  to: Scalars['DateTime'];
  tenantsWhere2: TenantWhereInput;
}>;


export type TenantsDataByCategoryQuery = { __typename?: 'Query', tenants?: Array<{ __typename?: 'Tenant', id: string, name?: string | null, resources?: Array<{ __typename?: 'Resource', id: string, name?: string | null, capacity?: number | null, unit?: ResourceUnitType | null, resourceCategory?: ResourceResourceCategoryType | null, deviceReadSum?: number | null, deviceReadAvg?: number | null }> | null }> | null };

export type WaterQualityDevicesDetailsQueryVariables = Exact<{
  where: DeviceWhereInput;
}>;


export type WaterQualityDevicesDetailsQuery = { __typename?: 'Query', devices?: Array<{ __typename?: 'Device', id: string, name?: string | null, deviceReadSum?: number | null, deviceReadAvg?: number | null, deviceType?: { __typename?: 'DeviceType', id: string, name?: string | null, scale?: any | null } | null }> | null };


export const AuthenticateUserWithPasswordDocument = `
    mutation AuthenticateUserWithPassword($email: String!, $password: String!) {
  authenticateUserWithPassword(email: $email, password: $password) {
    ... on UserAuthenticationWithPasswordSuccess {
      sessionToken
      item {
        name
        email
        id
        role
        tenant {
          id
          name
          status
        }
      }
    }
    ... on UserAuthenticationWithPasswordFailure {
      message
    }
  }
}
    `;
export const useAuthenticateUserWithPasswordMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<AuthenticateUserWithPasswordMutation, TError, AuthenticateUserWithPasswordMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<AuthenticateUserWithPasswordMutation, TError, AuthenticateUserWithPasswordMutationVariables, TContext>(
      ['AuthenticateUserWithPassword'],
      (variables?: AuthenticateUserWithPasswordMutationVariables) => fetcher<AuthenticateUserWithPasswordMutation, AuthenticateUserWithPasswordMutationVariables>(client, AuthenticateUserWithPasswordDocument, variables, headers)(),
      options
    );
export const SendUserPasswordResetLinkDocument = `
    mutation SendUserPasswordResetLink($email: String!) {
  sendUserPasswordResetLink(email: $email)
}
    `;
export const useSendUserPasswordResetLinkMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<SendUserPasswordResetLinkMutation, TError, SendUserPasswordResetLinkMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<SendUserPasswordResetLinkMutation, TError, SendUserPasswordResetLinkMutationVariables, TContext>(
      ['SendUserPasswordResetLink'],
      (variables?: SendUserPasswordResetLinkMutationVariables) => fetcher<SendUserPasswordResetLinkMutation, SendUserPasswordResetLinkMutationVariables>(client, SendUserPasswordResetLinkDocument, variables, headers)(),
      options
    );
export const AuthenticatedItemDocument = `
    query AuthenticatedItem {
  authenticatedItem {
    ... on User {
      id
      name
      email
      role
      status
      tenant {
        id
        name
        status
      }
    }
  }
}
    `;
export const useAuthenticatedItemQuery = <
      TData = AuthenticatedItemQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables?: AuthenticatedItemQueryVariables,
      options?: UseQueryOptions<AuthenticatedItemQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<AuthenticatedItemQuery, TError, TData>(
      variables === undefined ? ['AuthenticatedItem'] : ['AuthenticatedItem', variables],
      fetcher<AuthenticatedItemQuery, AuthenticatedItemQueryVariables>(client, AuthenticatedItemDocument, variables, headers),
      options
    );
export const UsersDocument = `
    query Users($where: UserWhereInput!, $skip: Int!, $take: Int, $orderBy: [UserOrderByInput!]!, $usersCountWhere2: UserWhereInput!) {
  users(where: $where, skip: $skip, take: $take, orderBy: $orderBy) {
    id
    name
    email
    role
    phone
    status
    tenant {
      id
      name
    }
  }
  usersCount(where: $usersCountWhere2)
}
    `;
export const useUsersQuery = <
      TData = UsersQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables: UsersQueryVariables,
      options?: UseQueryOptions<UsersQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<UsersQuery, TError, TData>(
      ['Users', variables],
      fetcher<UsersQuery, UsersQueryVariables>(client, UsersDocument, variables, headers),
      options
    );
export const TenantsDocument = `
    query Tenants($where: TenantWhereInput!, $orderBy: [TenantOrderByInput!]!, $take: Int, $skip: Int!, $tenantsCountWhere2: TenantWhereInput!) {
  tenants(where: $where, orderBy: $orderBy, take: $take, skip: $skip) {
    id
    name
    status
    location
    description
    owners {
      id
      name
    }
    facilities {
      id
      name
    }
    facilitiesCount
    parent {
      id
      name
    }
    resources {
      id
      name
      deviceReadSum
      resourceCategory
    }
  }
  tenantsCount(where: $tenantsCountWhere2)
}
    `;
export const useTenantsQuery = <
      TData = TenantsQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables: TenantsQueryVariables,
      options?: UseQueryOptions<TenantsQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<TenantsQuery, TError, TData>(
      ['Tenants', variables],
      fetcher<TenantsQuery, TenantsQueryVariables>(client, TenantsDocument, variables, headers),
      options
    );
export const CreateUserDocument = `
    mutation CreateUser($data: UserCreateInput!) {
  createUser(data: $data) {
    id
    name
    email
    phone
    status
  }
}
    `;
export const useCreateUserMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<CreateUserMutation, TError, CreateUserMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<CreateUserMutation, TError, CreateUserMutationVariables, TContext>(
      ['CreateUser'],
      (variables?: CreateUserMutationVariables) => fetcher<CreateUserMutation, CreateUserMutationVariables>(client, CreateUserDocument, variables, headers)(),
      options
    );
export const UpdateUserDocument = `
    mutation UpdateUser($where: UserWhereUniqueInput!, $data: UserUpdateInput!) {
  updateUser(where: $where, data: $data) {
    id
    name
    email
    phone
    role
    status
  }
}
    `;
export const useUpdateUserMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<UpdateUserMutation, TError, UpdateUserMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<UpdateUserMutation, TError, UpdateUserMutationVariables, TContext>(
      ['UpdateUser'],
      (variables?: UpdateUserMutationVariables) => fetcher<UpdateUserMutation, UpdateUserMutationVariables>(client, UpdateUserDocument, variables, headers)(),
      options
    );
export const LogoutDocument = `
    mutation logout {
  endSession
}
    `;
export const useLogoutMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<LogoutMutation, TError, LogoutMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<LogoutMutation, TError, LogoutMutationVariables, TContext>(
      ['logout'],
      (variables?: LogoutMutationVariables) => fetcher<LogoutMutation, LogoutMutationVariables>(client, LogoutDocument, variables, headers)(),
      options
    );
export const CreateTenantDocument = `
    mutation CreateTenant($data: TenantCreateInput!) {
  createTenant(data: $data) {
    id
    name
    location
    description
    status
    owners {
      id
      name
    }
  }
}
    `;
export const useCreateTenantMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<CreateTenantMutation, TError, CreateTenantMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<CreateTenantMutation, TError, CreateTenantMutationVariables, TContext>(
      ['CreateTenant'],
      (variables?: CreateTenantMutationVariables) => fetcher<CreateTenantMutation, CreateTenantMutationVariables>(client, CreateTenantDocument, variables, headers)(),
      options
    );
export const UpdateTenantDocument = `
    mutation UpdateTenant($where: TenantWhereUniqueInput!, $data: TenantUpdateInput!) {
  updateTenant(where: $where, data: $data) {
    id
    name
    location
    description
    status
  }
}
    `;
export const useUpdateTenantMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<UpdateTenantMutation, TError, UpdateTenantMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<UpdateTenantMutation, TError, UpdateTenantMutationVariables, TContext>(
      ['UpdateTenant'],
      (variables?: UpdateTenantMutationVariables) => fetcher<UpdateTenantMutation, UpdateTenantMutationVariables>(client, UpdateTenantDocument, variables, headers)(),
      options
    );
export const FacilitiesDocument = `
    query Facilities {
  facilities {
    id
    name
  }
}
    `;
export const useFacilitiesQuery = <
      TData = FacilitiesQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables?: FacilitiesQueryVariables,
      options?: UseQueryOptions<FacilitiesQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<FacilitiesQuery, TError, TData>(
      variables === undefined ? ['Facilities'] : ['Facilities', variables],
      fetcher<FacilitiesQuery, FacilitiesQueryVariables>(client, FacilitiesDocument, variables, headers),
      options
    );
export const CreateFacilityDocument = `
    mutation CreateFacility($data: FacilityCreateInput!) {
  createFacility(data: $data) {
    id
    name
    status
  }
}
    `;
export const useCreateFacilityMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<CreateFacilityMutation, TError, CreateFacilityMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<CreateFacilityMutation, TError, CreateFacilityMutationVariables, TContext>(
      ['CreateFacility'],
      (variables?: CreateFacilityMutationVariables) => fetcher<CreateFacilityMutation, CreateFacilityMutationVariables>(client, CreateFacilityDocument, variables, headers)(),
      options
    );
export const RedeemUserPasswordResetTokenDocument = `
    mutation RedeemUserPasswordResetToken($email: String!, $token: String!, $password: String!) {
  redeemUserPasswordResetToken(email: $email, token: $token, password: $password) {
    code
    message
  }
}
    `;
export const useRedeemUserPasswordResetTokenMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<RedeemUserPasswordResetTokenMutation, TError, RedeemUserPasswordResetTokenMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<RedeemUserPasswordResetTokenMutation, TError, RedeemUserPasswordResetTokenMutationVariables, TContext>(
      ['RedeemUserPasswordResetToken'],
      (variables?: RedeemUserPasswordResetTokenMutationVariables) => fetcher<RedeemUserPasswordResetTokenMutation, RedeemUserPasswordResetTokenMutationVariables>(client, RedeemUserPasswordResetTokenDocument, variables, headers)(),
      options
    );
export const TenantDetailsDocument = `
    query TenantDetails($where: TenantWhereUniqueInput!) {
  tenant(where: $where) {
    id
    name
    location
    description
    status
    owners {
      id
      name
    }
    facilities {
      id
      name
    }
    resources {
      id
      name
      resourceCategory
      capacity
      unit
      deviceReadSum
      deviceReadAvg
    }
    resourcesCount
    children {
      id
      name
      location
      description
      status
      owners {
        id
        name
      }
      facilities {
        id
        name
      }
    }
    childrenCount
  }
}
    `;
export const useTenantDetailsQuery = <
      TData = TenantDetailsQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables: TenantDetailsQueryVariables,
      options?: UseQueryOptions<TenantDetailsQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<TenantDetailsQuery, TError, TData>(
      ['TenantDetails', variables],
      fetcher<TenantDetailsQuery, TenantDetailsQueryVariables>(client, TenantDetailsDocument, variables, headers),
      options
    );
export const DevicesDocument = `
    query Devices($take: Int, $skip: Int!, $where: DeviceWhereInput!, $devicesCountWhere2: DeviceWhereInput!) {
  devices(take: $take, skip: $skip, where: $where) {
    id
    name
    deviceId
    edgeDeviceId
    portNumber
    description
    status
    deviceType {
      id
      name
    }
    facility {
      id
      name
    }
    resource {
      id
      name
      resourceCategory
    }
  }
  devicesCount(where: $devicesCountWhere2)
}
    `;
export const useDevicesQuery = <
      TData = DevicesQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables: DevicesQueryVariables,
      options?: UseQueryOptions<DevicesQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<DevicesQuery, TError, TData>(
      ['Devices', variables],
      fetcher<DevicesQuery, DevicesQueryVariables>(client, DevicesDocument, variables, headers),
      options
    );
export const CreateDeviceDocument = `
    mutation CreateDevice($data: DeviceCreateInput!) {
  createDevice(data: $data) {
    id
    deviceId
  }
}
    `;
export const useCreateDeviceMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<CreateDeviceMutation, TError, CreateDeviceMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<CreateDeviceMutation, TError, CreateDeviceMutationVariables, TContext>(
      ['CreateDevice'],
      (variables?: CreateDeviceMutationVariables) => fetcher<CreateDeviceMutation, CreateDeviceMutationVariables>(client, CreateDeviceDocument, variables, headers)(),
      options
    );
export const UpdateDeviceDocument = `
    mutation UpdateDevice($where: DeviceWhereUniqueInput!, $data: DeviceUpdateInput!) {
  updateDevice(where: $where, data: $data) {
    id
    deviceId
  }
}
    `;
export const useUpdateDeviceMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<UpdateDeviceMutation, TError, UpdateDeviceMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<UpdateDeviceMutation, TError, UpdateDeviceMutationVariables, TContext>(
      ['UpdateDevice'],
      (variables?: UpdateDeviceMutationVariables) => fetcher<UpdateDeviceMutation, UpdateDeviceMutationVariables>(client, UpdateDeviceDocument, variables, headers)(),
      options
    );
export const ResourcesDocument = `
    query Resources($where: ResourceWhereInput!, $take: Int, $skip: Int!, $resourcesCountWhere2: ResourceWhereInput!) {
  resources(where: $where, take: $take, skip: $skip) {
    id
    name
    resourceCategory
    capacity
    unit
    status
  }
  resourcesCount(where: $resourcesCountWhere2)
}
    `;
export const useResourcesQuery = <
      TData = ResourcesQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables: ResourcesQueryVariables,
      options?: UseQueryOptions<ResourcesQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<ResourcesQuery, TError, TData>(
      ['Resources', variables],
      fetcher<ResourcesQuery, ResourcesQueryVariables>(client, ResourcesDocument, variables, headers),
      options
    );
export const DeviceTypesDocument = `
    query DeviceTypes {
  deviceTypes {
    id
    name
  }
}
    `;
export const useDeviceTypesQuery = <
      TData = DeviceTypesQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables?: DeviceTypesQueryVariables,
      options?: UseQueryOptions<DeviceTypesQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<DeviceTypesQuery, TError, TData>(
      variables === undefined ? ['DeviceTypes'] : ['DeviceTypes', variables],
      fetcher<DeviceTypesQuery, DeviceTypesQueryVariables>(client, DeviceTypesDocument, variables, headers),
      options
    );
export const FacilitiesUnderTenantDocument = `
    query FacilitiesUnderTenant($where: FacilityWhereInput!) {
  facilities(where: $where) {
    id
    name
  }
}
    `;
export const useFacilitiesUnderTenantQuery = <
      TData = FacilitiesUnderTenantQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables: FacilitiesUnderTenantQueryVariables,
      options?: UseQueryOptions<FacilitiesUnderTenantQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<FacilitiesUnderTenantQuery, TError, TData>(
      ['FacilitiesUnderTenant', variables],
      fetcher<FacilitiesUnderTenantQuery, FacilitiesUnderTenantQueryVariables>(client, FacilitiesUnderTenantDocument, variables, headers),
      options
    );
export const CreateResourceDocument = `
    mutation CreateResource($data: ResourceCreateInput!) {
  createResource(data: $data) {
    id
    name
    status
    resourceCategory
  }
}
    `;
export const useCreateResourceMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<CreateResourceMutation, TError, CreateResourceMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<CreateResourceMutation, TError, CreateResourceMutationVariables, TContext>(
      ['CreateResource'],
      (variables?: CreateResourceMutationVariables) => fetcher<CreateResourceMutation, CreateResourceMutationVariables>(client, CreateResourceDocument, variables, headers)(),
      options
    );
export const UpdateResourceDocument = `
    mutation UpdateResource($where: ResourceWhereUniqueInput!, $data: ResourceUpdateInput!) {
  updateResource(where: $where, data: $data) {
    id
    name
    status
    resourceCategory
  }
}
    `;
export const useUpdateResourceMutation = <
      TError = unknown,
      TContext = unknown
    >(
      client: GraphQLClient,
      options?: UseMutationOptions<UpdateResourceMutation, TError, UpdateResourceMutationVariables, TContext>,
      headers?: RequestInit['headers']
    ) =>
    useMutation<UpdateResourceMutation, TError, UpdateResourceMutationVariables, TContext>(
      ['UpdateResource'],
      (variables?: UpdateResourceMutationVariables) => fetcher<UpdateResourceMutation, UpdateResourceMutationVariables>(client, UpdateResourceDocument, variables, headers)(),
      options
    );
export const ResourcesDataByDateDocument = `
    query ResourcesDataByDate($from: DateTime!, $to: DateTime!, $where: ResourceWhereInput!) {
  resources(where: $where) {
    id
    name
    status
    capacity
    unit
    resourceCategory
    deviceReadSum(from: $from, to: $to)
    deviceReadAvg(from: $from, to: $to)
    deviceReadCurrent(from: $from, to: $to)
  }
}
    `;
export const useResourcesDataByDateQuery = <
      TData = ResourcesDataByDateQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables: ResourcesDataByDateQueryVariables,
      options?: UseQueryOptions<ResourcesDataByDateQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<ResourcesDataByDateQuery, TError, TData>(
      ['ResourcesDataByDate', variables],
      fetcher<ResourcesDataByDateQuery, ResourcesDataByDateQueryVariables>(client, ResourcesDataByDateDocument, variables, headers),
      options
    );
export const TenantDetailsByDateDocument = `
    query TenantDetailsByDate($where: TenantWhereUniqueInput!, $from: DateTime!, $to: DateTime!, $deviceReadSumFrom2: DateTime!, $deviceReadSumTo2: DateTime!) {
  tenant(where: $where) {
    id
    name
    facilities {
      id
      name
      deviceReadSum(from: $from, to: $to)
      deviceReadAvg(from: $from, to: $to)
    }
    resources {
      id
      name
      status
      capacity
      unit
      resourceCategory
      deviceReadSum(from: $deviceReadSumFrom2, to: $deviceReadSumTo2)
      deviceReadAvg(from: $deviceReadSumFrom2, to: $deviceReadSumTo2)
      deviceReadCurrent(from: $deviceReadSumFrom2, to: $deviceReadSumTo2)
    }
  }
}
    `;
export const useTenantDetailsByDateQuery = <
      TData = TenantDetailsByDateQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables: TenantDetailsByDateQueryVariables,
      options?: UseQueryOptions<TenantDetailsByDateQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<TenantDetailsByDateQuery, TError, TData>(
      ['TenantDetailsByDate', variables],
      fetcher<TenantDetailsByDateQuery, TenantDetailsByDateQueryVariables>(client, TenantDetailsByDateDocument, variables, headers),
      options
    );
export const TenantsByDateDocument = `
    query TenantsByDate($where: TenantWhereInput!, $from: DateTime!, $to: DateTime!, $deviceReadSumFrom2: DateTime!, $deviceReadSumTo2: DateTime!) {
  tenants(where: $where) {
    id
    name
    facilities {
      id
      name
      deviceReadSum(from: $deviceReadSumFrom2, to: $deviceReadSumTo2)
      deviceReadAvg(from: $deviceReadSumFrom2, to: $deviceReadSumTo2)
    }
    resources {
      id
      name
      deviceReadSum(from: $from, to: $to)
      deviceReadAvg(from: $from, to: $to)
      capacity
      unit
    }
  }
}
    `;
export const useTenantsByDateQuery = <
      TData = TenantsByDateQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables: TenantsByDateQueryVariables,
      options?: UseQueryOptions<TenantsByDateQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<TenantsByDateQuery, TError, TData>(
      ['TenantsByDate', variables],
      fetcher<TenantsByDateQuery, TenantsByDateQueryVariables>(client, TenantsByDateDocument, variables, headers),
      options
    );
export const TenantsDataByCategoryDocument = `
    query TenantsDataByCategory($where: ResourceWhereInput!, $from: DateTime!, $to: DateTime!, $tenantsWhere2: TenantWhereInput!) {
  tenants(where: $tenantsWhere2) {
    id
    name
    resources(where: $where) {
      id
      name
      capacity
      unit
      resourceCategory
      deviceReadSum(from: $from, to: $to)
      deviceReadAvg(from: $from, to: $to)
    }
  }
}
    `;
export const useTenantsDataByCategoryQuery = <
      TData = TenantsDataByCategoryQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables: TenantsDataByCategoryQueryVariables,
      options?: UseQueryOptions<TenantsDataByCategoryQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<TenantsDataByCategoryQuery, TError, TData>(
      ['TenantsDataByCategory', variables],
      fetcher<TenantsDataByCategoryQuery, TenantsDataByCategoryQueryVariables>(client, TenantsDataByCategoryDocument, variables, headers),
      options
    );
export const WaterQualityDevicesDetailsDocument = `
    query WaterQualityDevicesDetails($where: DeviceWhereInput!) {
  devices(where: $where) {
    id
    name
    deviceReadSum
    deviceReadAvg
    deviceType {
      id
      name
      scale
    }
  }
}
    `;
export const useWaterQualityDevicesDetailsQuery = <
      TData = WaterQualityDevicesDetailsQuery,
      TError = unknown
    >(
      client: GraphQLClient,
      variables: WaterQualityDevicesDetailsQueryVariables,
      options?: UseQueryOptions<WaterQualityDevicesDetailsQuery, TError, TData>,
      headers?: RequestInit['headers']
    ) =>
    useQuery<WaterQualityDevicesDetailsQuery, TError, TData>(
      ['WaterQualityDevicesDetails', variables],
      fetcher<WaterQualityDevicesDetailsQuery, WaterQualityDevicesDetailsQueryVariables>(client, WaterQualityDevicesDetailsDocument, variables, headers),
      options
    );