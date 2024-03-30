import sort from './sort.js';

/**
 * Sorts the given array of values by a key attribute using the
 * given direction. Optionally also filters only values whose
 * attribute values are "before" or "after" of the given 'since' value
 * depending on the direction.
 */
export default function order<T, K extends keyof T>(
  values: T[],
  ordering: K,
  direction: 'asc' | 'desc',
  since?: T[K],
): T[] {
  return sort(values, (item) => item[ordering], direction, since);
}
