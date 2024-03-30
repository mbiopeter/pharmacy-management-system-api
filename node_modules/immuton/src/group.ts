import propertyless from './propertyless.js';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default function group<K extends keyof any, T>(
  values: T[],
  selector: (item: T, index: number) => K,
): { [P in K]: T[] } {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let result: any;
  values.forEach((value, index) => {
    const key = selector(value, index);
    if (!result) {
      result = {};
    }
    // eslint-disable-next-line no-multi-assign
    const acc = (result[key] = result[key] || ([] as T[]));
    acc.push(value);
  });
  return result || propertyless;
}
