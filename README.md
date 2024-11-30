# Budget App POC

## Prerequisites

- `uv`
- `pnpm`
- `nvm`

## How To Run

### Backend

```bash
cp api/.env.example api/.env
docker compose up --build
```

### Frontend

```bash
nvm use
pnpm i
pnpm run dev
```

## How to Run Django Commands

```bash
docker compose run --rm django python manage.py <command>
```

## Apps and Packages

- `web`: another [Next.js](https://nextjs.org/) app
- `@repo/ui`: a shared shadcn React component library
- `@repo/eslint-config`: `eslint` configurations (includes `eslint-config-next` and `eslint-config-prettier`)
- `@repo/typescript-config`: `tsconfig.json`s used throughout the monorepo

### Build

To build all apps and packages, run the following command:

```bash
pnpm run build
```
