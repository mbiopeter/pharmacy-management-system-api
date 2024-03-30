import hasOwnProperty from './hasOwnProperty.js';
import propertyless from './propertyless.js';

/* eslint-disable no-restricted-syntax */
/**
 * Returns a copy of the object that contains all of its properties except the ones
 * listed as a parameter. If the object has not any of the omitted properties, then
 * the original reference is returned.
 * @param obj object whose properties to omit
 * @param props property names to omit
 */
export default function omit<T, K extends keyof T>(obj: T, props: K[]): Omit<T, K> {
  if (props.every((prop) => !hasOwnProperty(obj, prop))) {
    return obj;
  }
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let output: any;
  for (const key in obj) {
    if (hasOwnProperty(obj, key) && (props as Array<keyof T>).indexOf(key) < 0) {
      // At least one property will be omitted
      output = output || ({} as Omit<T, K>);
      output[key] = obj[key];
    }
  }
  return output || propertyless;
}
