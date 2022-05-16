import { CSSProperties, SetStateAction } from 'react';
import moment from 'moment';
import {
  OrderDirection,
  ResourceResourceCategoryType,
  ResourceUnitType,
  UserRoleType,
  UserStatusType,
} from '@api/graphql';

export type LoginFormInputs = {
  username: string;
  password: string;
};
export type FormInputs = {
  fullName?: string;
  email: string;
  phone: string;
  password: string;
  confirmPassword?: string;
};
export const globalVariables = {
  nameRequired: 'Full Name is required',
  nameValidation: 'Only alphabets are allowed for this field',
  emailRequired: 'Email is required',
  emailValidation: 'Email is invalid',
  phoneRequired: 'Phone Number is required',
  phoneValidation:
    'Phone Number is invalid, must contain only numbers and length of 10 digits',
  passwordRequired: 'Password is required',
  passwordValidation:
    'Must Contain 8 Characters, One Uppercase, One Lowercase, One Number and One Special Case Character',
  confirmPasswordRequired: 'Confirm Password is required',
  confirmPasswordValidation: 'Passwords must match',
  user: 'Select User',
  parent: 'Select Parent',
  deviceIdRequired: 'Device Id is required',
  edgeDeviceIdRequired: 'Edge Device Id is required',
  devicePortRequired: 'Device Port Number is required',
  descriptionRequired: 'Description is required',
  resource: 'Select Resource',
  sensorType: 'Sensor Type',
  categoryType: 'Select Category',
  resourceType: 'Resource Type',
  tenantFacility: 'Tenant Facility',
  tenant: 'tenant',
  water: 'Water',
  power: 'Power',
  sewage: 'Sewage Treatment',
  home: 'home',
  tenantName: 'Tenant Name is required',
  location: 'Location is required',
  owner: 'User is required',
  description: 'Description is required',
  facilities: 'Facilities is required',
  deviceNameRequired: 'Device Name is required',
};
export const messages = {
  updateMessage: 'User updated successfully !',
  userDeleteMessage: 'User Deleted Successfully.',
  userDeactivatedMessage: 'User Deactivated Successfully',
  userActivatedMessage: 'User Activated Successfully',
  userUnBlockeMessage: 'User Unblocked Successfully',
  commonError: 'Something went wrong. Please try again !',
  usercreatedMessage: 'User Created Successfully',
  tenantCreateMessage: 'Tenant Created Successfully',
  tenantUpdateMessage: 'Tenant updated successfully',
  tenantDeactivateMessage: 'Tenant Deactivated Successfully',
  tenantActiveMessage: 'Tenant Activated Successfully',
  sensorCreateMessage: 'Sensor Created Successfully',
  sensorUpdateMessage: 'Sensor Updated Successfully',
  sensorDeactivateMessage: 'Sensor Deactivated Successfully',
  sensorActiveMessage: 'Sensor Activated Successfully',
};
export type UsersType =
  | {
      id: string;
      name?: string;
      email?: string;
      phone?: string;
      role?: UserRoleType;
      status?: UserStatusType;
    }
  | null
  | undefined;

export const status = {
  active: 'active',
  error: 'error',
  success: 'success',
  blocked: 'blocked',
  delete: 'delete',
  deactivate: 'deactivate',
};
export const PageNames = {
  home: 'Home',
  user: 'User',
  tenant: 'Tenant',
  sensors: 'Sensors',
  settings: 'Settings',
};
export type userTableType = {
  name?: string | null | undefined;
  email?: string | null | undefined;
  id: string;
  role?: UserRoleType | null | undefined;
  userUploadsCount?: number | null | undefined;
  userTemplatesCount?: number | null | undefined;
  status?: UserStatusType | null | undefined;
};
export type userTableHeader = {
  value: string;
  label: string;
};

export const orderAsc = [
  {
    name: OrderDirection.Asc,
  },
];

export const commonWhere = {
  name: {
    contains: '',
  },
};

export type TenantFormInputs = {
  name: string;
  location: string;
  owner: string;
  parent: string;
  description: string;
  facilities: any /* will do it later */;
};

export type tenantType = {
  id: SetStateAction<string>;
  facilities: { id: string; name: string }[];
  name: string;
  location: string;
  owners: { id: string }[];
  parent: { id: string };
  description: string;
  resources: {
    id: string;
    name: string;
    deviceReadSum: number;
    resourceCategory: ResourceResourceCategoryType;
  }[];
};

export type SensorFormType = {
  deviceName: string;
  deviceId: string;
  edgeDeviceId: string;
  portNumber: string;
  sensorType: string;
  resourceType: string;
  resource: string;
  tenant: string;
  facility?: string;
  description: string;
};

export type DeviceType = {
  id: string | null | undefined;
  name: string | null | undefined;
  deviceId: string | null | undefined;
  edgeDeviceId: string | null | undefined;
  portNumber: string | null | undefined;
  deviceType: { id: string; name: string } | null | undefined;
  resourceType: { id: string; name: string } | null | undefined;
  resource:
    | { id: string; name: string; resourceCategory: string }
    | null
    | undefined;
  tenant: { id: string; name: string } | null | undefined;
  facility: { id: string; name: string } | null | undefined;
  description: string | null | undefined;
};

export type tenantData = {
  name: string;
  location: string;
  description: string;
  owners?: {
    connect: {
      id: string;
    }[];
  } | null;
  facilities: {
    connect: {
      id: string;
    }[];
    disconnect?: {
      id: string;
    }[];
  };
  parent?: {
    connect: {
      id: string;
    };
  };
};

export type tenantOptionalFields = {
  deviceType?: {
    connect: {
      id: string;
    };
  };
  tenant?: {
    connect: {
      id: string;
    };
  };
  facility?: {
    connect: {
      id: string;
    };
  };
  resource?: {
    connect: {
      id: string;
    };
  };
};

export interface MyCustomCSS extends CSSProperties {
  '--value': number;
}

export type resourceType =
  | {
      __typename?: 'Resource';
      id: string;
      name?: string;
      resourceCategory?: ResourceResourceCategoryType;
      capacity?: number;
      unit?: ResourceUnitType;
      deviceReadSum?: number;
      deviceReadAvg?: number;
    }[]
  | null
  | undefined;

export type resourceDataType = {
  __typename?: 'Resource';
  id: string;
  name?: string | null;
  resourceCategory?: ResourceResourceCategoryType | null;
  capacity?: number | null;
  unit?: ResourceUnitType | null;
  deviceReadSum?: number | null;
  deviceReadAvg?: number | null;
  deviceReadCurrent?: number | null;
} | null;

export type facilityType =
  | {
      __typename?: 'Facility';
      id: string;
      name?: string | null;
      deviceReadSum?: number | null;
      deviceReadAvg?: number | null;
    }[]
  | null
  | undefined;

export const dateBeforeOneWeek = moment()
  .subtract(7, 'days')
  .endOf('day')
  .format();
export const todayDate = moment().format();

export type waterQualityType = {
  __typename?: 'Device';
  id: string;
  name?: string;
  deviceReadSum?: number;
  deviceReadAvg?: number;
  deviceType?: {
    __typename?: 'DeviceType';
    id: string;
    name?: string;
    scale?: {
      low: number;
      high?: number;
    };
  };
};

export type selectType = { value: any; label?: string };
