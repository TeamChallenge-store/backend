# Description

### Online store

```
  Description...
```

# Requirements

- [Node.js](https://nodejs.org/download/release/v21.5.0/) (recommended version: 21.5.0)
- [npm](https://www.npmjs.com/package/npm/v/10.2.4) (recommended version: 10.2.4)
- [linter](https://www.npmjs.com/package/@mate-academy/eslint-config-react-typescript) (using mate-academy config)
- [prettier](https://prettier.io/) ![Alt text](https://i.imgur.com/W9Qr0HS.png)
- [husky](https://www.npmjs.com/package/husky/v/8.0.3/) (install and check it)

# Installation

1. Clone the repository:

```bash
  git clone https://github.com/TeamChallenge-store/client.git
```

2. Go to your local folder

```bash
  cd "project name"
```

3. Installing dependencies

```bash
  npm i
```

# Scripts

- `dev`: Runs the application in development mode using Vite.
- `build`: Builds the project using TypeScript (tsc) and then uses Vite to build the final version of the project.

- `lint`: Runs ESLint for static code analysis.

- `format`: Runs Prettier to format code according to rules.

- `fix-style`: Runs npm run format and npm run lint scripts to automatically fix code style.

- `deploy`: Deploys the application to GitHub Pages.

- `predeploy`: Runs before the deploy script. In this case,  
  it runs an npm run build to ensure that the latest version of the code is used before publishing.

- `prepare`: Installs Husky, a tool for managing git hooks. Called when a package is installed and runs husky install.

# Project structure

- `/public` - static resources
- `/dist` - deploy folder
- `/src` - application source code
  [fsd](https://feature-sliced.design/ru/docs/get-started/overview)
  - `~app`
  - `~pages`
  - `~widgets`
  - `~entities`
  - `~features`
  - `~shared`

# Commits style guide

- According to [conventional](https://www.conventionalcommits.org/en/v1.0.0/)

- Also u need to add time stamp ($(LC_TIME=en_US.UTF-8 date '+%a, %b %d, %Y %I:%M:%S %p')). It works in bash
