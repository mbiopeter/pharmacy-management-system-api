# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.1.1

### Fixed

- Fix importing from the package by declaring the missing `main`, `module` and `types` in `package.json`

## 0.1.0

### Added

- First release with the basic **validation**, **serialization** and **deserialization** support
- The first collection of supported fields:
  - `string`
  - `choice`
  - `constant`
  - `integer`
  - `number`
  - `decimal`
  - `boolean`
  - `matching`
  - `datetime`
  - `date`
  - `timestamp`
  - `uuid`
  - `email`
  - `url`
  - `nullable`
  - `list`
