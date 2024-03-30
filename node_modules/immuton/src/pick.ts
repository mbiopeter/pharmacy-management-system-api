import hasOwnProperty from './hasOwnProperty.js';
import propertyless from './propertyless.js';

/* eslint-disable no-restricted-syntax */
/**
 * Returns a copy of the object that only contains the given property names, if present.
 * If the object has no other properties, then the original reference is returned.
 * @param obj object whose properties to pick
 * @param props property names to pick
 */
export default function pick<T, K extends keyof T>(obj: T, props: K[]): Pick<T, K> {
  for (const key in obj) {
    if ((props as Array<keyof T>).indexOf(key) < 0) {
      // At least one property will be omitted
      let output: Pick<T, K> | undefined;
      props.forEach((propName) => {
        if (hasOwnProperty(obj, propName)) {
          output = output || ({} as Pick<T, K>);
          output[propName] = obj[propName];
        }
      });
      return output || (propertyless as Pick<T, K>);
    }
  }
  return obj as Pick<T, K>;
}
