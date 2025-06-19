// User types and interfaces for the application

export interface User {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  avatar?: string;
  department: string;
  role: UserRole;
  bio?: string;
  lastActive: string;
  isActive: boolean;
  permissions: Permission[];
}

export type UserRole = 'admin' | 'manager' | 'employee' | 'contractor';

export interface Permission {
  id: string;
  name: string;
  description: string;
  resource: string;
  actions: PermissionAction[];
}

export type PermissionAction = 'create' | 'read' | 'update' | 'delete';

export interface ApiResponse<T> {
  success: boolean;
  result: T;
  error?: string;
  message?: string;
  timestamp: string;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Generic utility types
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

export type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>;

export interface BaseEntity {
  id: number;
  createdAt: string;
  updatedAt: string;
  createdBy: number;
  updatedBy?: number;
}

// Form types
export type UserFormData = Optional<User, 'id' | 'lastActive' | 'isActive'>;

export interface LoginCredentials {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface AuthToken {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
  tokenType: 'Bearer';
}

// Event types
export interface UserEvent {
  type: 'user_created' | 'user_updated' | 'user_deleted' | 'user_login' | 'user_logout';
  userId: number;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

// Validation schemas using type-based approach
export const UserRoles: readonly UserRole[] = ['admin', 'manager', 'employee', 'contractor'] as const;

export const PermissionActions: readonly PermissionAction[] = ['create', 'read', 'update', 'delete'] as const;

// Type guards
export function isValidUserRole(role: string): role is UserRole {
  return UserRoles.includes(role as UserRole);
}

export function isValidPermissionAction(action: string): action is PermissionAction {
  return PermissionActions.includes(action as PermissionAction);
}

// Advanced types using generics and conditional types
export type ExtractArrayType<T> = T extends (infer U)[] ? U : never;

export type KeysOfType<T, U> = {
  [K in keyof T]: T[K] extends U ? K : never;
}[keyof T];

export type NonNullable<T> = T extends null | undefined ? never : T;

// Branded types for type safety
export type UserId = number & { readonly brand: unique symbol };
export type Email = string & { readonly brand: unique symbol };

export function createUserId(id: number): UserId {
  return id as UserId;
}

export function createEmail(email: string): Email {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    throw new Error('Invalid email format');
  }
  return email as Email;
}

// Mapped types for form state management
export type FormErrors<T> = {
  [K in keyof T]?: string;
};

export type FormTouched<T> = {
  [K in keyof T]?: boolean;
};

export interface FormState<T> {
  values: T;
  errors: FormErrors<T>;
  touched: FormTouched<T>;
  isSubmitting: boolean;
  isValid: boolean;
}

// Async state management types
export interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  lastFetched?: string;
}

export type AsyncAction<T> = 
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: T }
  | { type: 'FETCH_ERROR'; payload: string }
  | { type: 'RESET' };

// Configuration types
export interface AppConfig {
  api: {
    baseUrl: string;
    timeout: number;
    retries: number;
  };
  features: {
    enableUserProfiles: boolean;
    enableNotifications: boolean;
    enableAnalytics: boolean;
  };
  ui: {
    theme: 'light' | 'dark' | 'auto';
    language: string;
    pageSize: number;
  };
}

// Export everything as a namespace for organized imports
export namespace Types {
  export type {
    User,
    UserRole,
    Permission,
    PermissionAction,
    ApiResponse,
    PaginatedResponse,
    UserFormData,
    LoginCredentials,
    AuthToken,
    UserEvent,
    FormState,
    AsyncState,
    AppConfig
  };
}