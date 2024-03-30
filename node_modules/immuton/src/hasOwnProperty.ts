const objectHasOwnProperty = Object.prototype.hasOwnProperty;

function hasOwnProperty(obj: null | undefined, propName: PropertyKey): false;
function hasOwnProperty<T, K extends PropertyKey>(obj: T, propName: K): obj is T & Record<K, unknown>;
function hasOwnProperty<T, K extends PropertyKey>(obj: T, propName: K): propName is K & keyof T;
function hasOwnProperty<T, K extends PropertyKey>(obj: T, propName: K): propName is K & keyof T {
  return obj != null && objectHasOwnProperty.call(obj, propName);
}

export default hasOwnProperty;
