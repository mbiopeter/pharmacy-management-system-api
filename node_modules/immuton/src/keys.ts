import empty from './empty.js';
import type { Key } from './types.js';

/**
 * Returns an array of own enumerable string properties of the given object.
 * This is a wrapper around Object.keys(…) that has a stricter return value
 * type and will also return the empty array singleton if the object has no
 * own enumerable string properties.
 * @param obj object whose properties to return
 */
export default function keys<T>(obj: T): Key<T>[] {
  const props = Object.keys(obj) as Key<T>[];
  return props.length ? props : empty;
}
