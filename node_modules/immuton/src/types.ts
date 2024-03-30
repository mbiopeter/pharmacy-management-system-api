export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<T>;
export type Require<T, K extends keyof T> = Pick<T, K> & Partial<T>;
export type Nullable<T> = { [P in keyof T]: T[P] | null };
export type Propertyless = Record<never, never>;
export type Key<T> = keyof T & string;
export type Exact<T, R, E = 'Object must only have allowed properties'> = T &
  (Exclude<keyof T, keyof R> extends never ? T : E);

/**
 * Resolves to keys of an object that match the given Condition type.
 * Source: https://medium.com/dailyjs/typescript-create-a-condition-based-subset-types-9d902cea5b8c
 */
export type FilteredKeys<T, Condition> = {
  [P in keyof T]: T[P] extends Condition ? P : never;
}[keyof T];
/**
 * Filters keys of an object so that they must match the given Condition type.
 * Source: https://medium.com/dailyjs/typescript-create-a-condition-based-subset-types-9d902cea5b8c
 */
export type FilteredValues<T, Condition> = Pick<T, FilteredKeys<T, Condition>>;

/**
 * Resolves to keys of an object that do NOT match the given Condition type.
 * Source: https://medium.com/dailyjs/typescript-create-a-condition-based-subset-types-9d902cea5b8c
 */
export type ExcludedKeys<T, Condition> = {
  [P in keyof T]: T[P] extends Condition ? never : P;
}[keyof T];
/**
 * Filters keys of an object so that they do NOT match the given Condition type.
 * Source: https://medium.com/dailyjs/typescript-create-a-condition-based-subset-types-9d902cea5b8c
 */
export type ExcludedValues<T, Condition> = Pick<T, ExcludedKeys<T, Condition>>;
