export default function isNotNull<T>(value: T): value is Exclude<T, null> {
  return value !== null;
}
