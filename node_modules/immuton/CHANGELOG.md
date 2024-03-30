# Changelog

All notable changes to this project will be documented in this file.

## 2.0.0

### Changed

- **Breaking change**: the library is now ESM only, and requires Node version 14 or newer.

### Fixed

- Fixed ordering of equal items in [`sort`](./src/sort.ts) and [`order`](./src/order.ts) with descending direction

## 1.2.0

### Changed

- Improved [`hasOwnProperty`](./src/hasOwnProperty.ts) type-guarding

## 1.1.2

### Fixed

- Fixed recursive usage of [`sort`](./src/sort.ts)

## 1.1.1

### Fixed

- Fixed [`hasProperties`](./src/hasProperties.ts) parameter typing

## 1.1.0

### Added

- [`isEmpty`](./src/isEmpty.ts)
- [`keys`](./src/keys.ts)

### Changed

- [`empty`](./src/empty.ts) singleton is now frozen, preventing accidental mutations
- [`propertyless`](./src/propertyless.ts) singleton is now frozen, preventing accidental mutations

## 1.0.2

### Fixed

- Fixed [`transform`](./src/transform.ts) missing unchanged values

## 1.0.1

### Fixed

- Fixed [`select`](./src/select.ts) parameter typing

## 1.0.0

### Added

- [`append`](./src/append.ts)
- [`build`](./src/build.ts)
- [`concat`](./src/concat.ts)
- [`difference`](./src/difference.ts)
- [`differenceBy`](./src/differenceBy.ts)
- [`editProperty`](./src/editProperty.ts)
- [`empty`](./src/empty.ts)
- [`extend`](./src/extend.ts)
- [`filter`](./src/filter.ts)
- [`findLastIndex`](./src/findLastIndex.ts)
- [`findOrderedIndex`](./src/findOrderedIndex.ts)
- [`flatMap`](./src/flatMap.ts)
- [`flatten`](./src/flatten.ts)
- [`group`](./src/group.ts)
- [`hasOwnProperty`](./src/hasOwnProperty.ts)
- [`hasProperties`](./src/hasProperties.ts)
- [`includes`](./src/includes.ts)
- [`isDefined`](./src/isDefined.ts)
- [`isEqual`](./src/isEqual.ts)
- [`isNotNull`](./src/isNotNull.ts)
- [`isNotNully`](./src/isNotNully.ts)
- [`isNull`](./src/isNull.ts)
- [`isNully`](./src/isNully.ts)
- [`isUndefined`](./src/isUndefined.ts)
- [`map`](./src/map.ts)
- [`mapFilter`](./src/mapFilter.ts)
- [`mapObject`](./src/mapObject.ts)
- [`objectDifference`](./src/objectDifference.ts)
- [`omit`](./src/omit.ts)
- [`order`](./src/order.ts)
- [`pick`](./src/pick.ts)
- [`propertyless`](./src/propertyless.ts)
- [`reject`](./src/reject.ts)
- [`select`](./src/select.ts)
- [`set`](./src/set.ts)
- [`slice`](./src/slice.ts)
- [`sort`](./src/sort.ts)
- [`splice`](./src/splice.ts)
- [`transform`](./src/transform.ts)
- [`union`](./src/union.ts)
