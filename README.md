<!-- markdownlint-disable MD033 -->

# Forge Style Guide

A style guide provides resources and shared consensus on best practices, formatting, and development practices. That requires having a deep understanding and experience with the platform and tools for which the guide speaks to. This style guide is built upon the ongoing experiences of the Valiantys engineering team with enterprise-grade software development built on the Forge platform. It is intended to be published as a “living” document in collaboration with marketplace vendors, Atlassian engineers, and customer development teams to evolve and grow along with the platform.

## Purpose

This guide seeks to provide an opinionated stance on syntax, conventions, and structure for solutions built on the Forge platform. The key driver for such a guide is to enhance and grow the Atlassian Cloud platform by lowering the barrier of entry for Forge development while spurring conversation and provoking thought around best practices and conventions.

## Community Contributions

It is a goal for this style guide to build upon the already strong community that exists around Forge to build shared resources backed by the people for whom it matters most. With Forge being a relatively new platform, we expect there to be growth and evolution within the platform that we intend to capture in the style guide. Community involvement is what takes this guide from being a blog post to being an ever-growing resource that creates adoption and engagement for the Forge platform.

[If you would like to contribute to the Forge Style Guide, click here to visit the public community-based Github repo.](https://github.com/valiantys-open-source/forge-style-guide)

## The Team

<table id="teamTable">
  <tr>
    <td><img src="./team/zishan-aslam.jpg" alt="Zishan Aslam" width="150"></td>
    <td><img src="./team/joshua-demetri.png" alt="Joshua Demetri" width="150"></td>
    <td><img src="./team/zachary-kipping.png" alt="Zachary Kipping" width="150"></td>
    <td><img src="./team/paul-spears.png" alt="Paul Spears" width="150"></td>
    <td><img src="./team/conner-mcneil.png" alt="Conner McNeil" width="150"></td>
  </tr>
  <tr>
    <td><b>Zishan Aslam</b><br>Software Architect</td>
    <td><b>Joshua Demetri</b><br>Principal Solutions Architect</td>
    <td><b>Zachary Kipping</b><br>R&D Manager</td>
    <td><b>Paul Spears</b><br>Head of R&D and Solution Architecture</td>
    <td><b>Conner McNeil</b><br>Head of Platform Development</td>
  </tr>
</table>

## Table of Contents

- [Single Purpose Code](#single-purpose-code)
- [Folder Architecture](#folder-architecture)
- [Manifest File Pointers](#manifest-file-pointers)
- [Module Amount Limitations](#module-amount-limitations)
- [Working With Teams](#working-with-teams)
- [Deploying to Forge](#deploying-to-forge)
- [Security Measures](#security-measures)
- [UI Kit vs Custom UI](#ui-kit-vs-custom-ui)
- [Forge Storage: Key Value vs Entity](#forge-storage-key-value-vs-entity-storage)
- [Contact Us / Feedback](#contact)

## Single Purpose Code

One of the most important aspects of having easy-to-read and debug code is to keep code minimal and serving a single purpose.

- **<green>Do</green>** keep each file limited to one function.
- **<green>Do</green>** keep each file limited to a single component.

### Single Function Per File

**<red>Incorrect:</red>**

```typescript
// src/triggers/web/multi-functions.ts
export async function handleWebTrigger(event: any): Promise<void> {
  console.log("Handling web trigger:", event);
}

export async function handleSecondWebTrigger(event: any): Promise<void> {
  console.log("Handling second web trigger:", event);
}
```

This example includes two functions in one file, violating the single-purpose rule.

**<green>Correct:</green>**

```typescript
// src/triggers/web/handleWebTrigger.ts
export async function handleWebTrigger(event: any): Promise<void> {
  console.log("Handling web trigger:", event);
}
```

```typescript
// src/triggers/web/handleSecondWebTrigger.ts
export async function handleSecondWebTrigger(event: any): Promise<void> {
  console.log("Handling second web trigger:", event);
}
```

Each file contains a single function, adhering to the single-purpose code guideline.

### Single Component Per File

**<red>Incorrect:</red>**

```typescript
// src/components/MultiComponents.tsx
import ForgeUI, { Button, Text } from "@forge/react";

const MyButton = () => {
  return (
    <Button text="Click Me" onClick={() => console.log("Button clicked!")} />
  );
};

const MyText = () => {
  return <Text content="Hello, World!" />;
};
```

This file contains two components, violating the guideline to keep one component per file.

**<green>Correct:</green>**

```typescript
// src/components/MyButton.tsx
import { Button } from "@forge/react";

const MyButton = () => {
  return (
    <Button text="Click Me" onClick={() => console.log("Button clicked!")} />
  );
};

export default MyButton;
```

```typescript
// src/components/MyText.tsx
import { Text } from "@forge/react";

const MyText = () => {
  return <Text content="Hello, World!" />;
};

export default MyText;
```

Each component is separated into its own file, following the single-purpose rule.

## Folder Architecture

Having each function/component separate per file can create a lot of files, so you need to maintain a good and easy-to-understand folder architecture. This architecture should ideally tell you exactly what is inside that folder without you even needing to open it. Keep backend code inside a folder marked as `src/backend` and the frontend code in `src/frontend`.

- **<green>Do</green>** keep all forge functions in a file suffixed with `.forge.ts` such as `filename.forge.ts`.
- **<green>Do</green>** keep all code within the `src` folder.
- **<green>Do</green>** keep all backend code inside a `src/backend` folder and all frontend code in `src/frontend`.
- **<green>Do</green>** keep each file name prefixed with the forge module.
  - src/backend/web-func-name.forge.ts
  - src/backend/web-2nd-func-name.forge.ts
  - src/backend/scheduled-func-name.forge.ts

**<red>Incorrect:</red>**

```bash
src/
│
├── func-name.ts
├── second-func-name.ts
└── frontend/
    ├── app.tsx
```

- Backend and frontend code are mixed in the root src/ directory.
- File names lack proper prefixes and suffixes.
- It’s not immediately clear whether these files belong to backend or frontend functionality.

**<green>Correct:</green>**

```bash
src/
│
├── backend/
│   ├── feature-name/
│       ├── web-func-name.forge.ts
│       ├── web-2nd-func-name.forge.ts
│       └── scheduled-func-name.forge.ts
│   ├── feature-2-name/
│       ├── web-func-name.forge.ts
│       ├── web-2nd-func-name.forge.ts
│       └── scheduled-func-name.forge.ts
└── frontend/
    ├── app.component.tsx
    └── header.component.tsx
```

<!-- TODO: Add a note/example of how to implement with and app that has multiple frontends -->

This separates backend and frontend code into distinct folders (src/backend and src/frontend) and uses clear file naming conventions with the `.forge.ts` suffix and module prefixes (web-, scheduled-). This structure is immediately intuitive and makes it easier to understand the contents of each folder.

## Manifest File Pointers

In the manifest file, you often need to specify a path to a function in your code. To avoid typos in the path, it is cleaner and easier to have everything exported in your index file. This way, your manifest file can always use the index file as the path.

- **<green>Do</green>** use the index file as the source of all functions in your manifest file.
- **<green>Do</green>** export all code that the manifest file needs in your index file.

### Barrel File Exports

**<red>Incorrect:</red>**

```typescript
// src/backend/web-func-name.forge.ts
export async function handleWebFunction(event: any): Promise<void> {
  console.log("Handling web trigger:", event);
}
```

```typescript
// src/backend/web-2nd-func-name.forge.ts
export async function handleSecondWebFunction(event: any): Promise<void> {
  console.log("Handling second web trigger:", event);
}
```

```typescript
// src/backend/scheduled-func-name.forge.ts
export async function handleScheduledFunction(event: any): Promise<void> {
  console.log("Handling scheduled trigger:", event);
}
```

**<green>Correct:</green>**

```typescript
// src/backend/web-func-name.forge.ts
export async function handleWebFunction(event: any): Promise<void> {
  console.log("Handling web trigger:", event);
}
```

```typescript
// src/backend/web-2nd-func-name.forge.ts
export async function handleSecondWebFunction(event: any): Promise<void> {
  console.log("Handling second web trigger:", event);
}
```

```typescript
// src/backend/scheduled-func-name.forge.ts
export async function handleScheduledFunction(event: any): Promise<void> {
  console.log("Handling scheduled trigger:", event);
}
```

```typescript
// src/index.ts
export { handleWebFunction } from "./web-func-name.forge";
export { handleSecondWebFunction } from "./web-2nd-func-name.forge";
export { handleScheduledFunction } from "./scheduled-func-name.forge";
```

The barrel file in `src/index.ts` re-exports all the Forge backend functions.
Each Forge function file (e.g., `web-func-name.forge.ts`) exports its function individually, but the barrel file consolidates them in one place for easier reference in other parts of the project, such as the manifest file.

**<red>Incorrect:</red>**

```yaml
# manifest.yml
modules:
  function:
    - key: web-function
      handler: src/backend/web-func-name.forge.handleWebFunction
    - key: second-web-function
      handler: src/backend/web-2nd-func-name.forge.handleSecondWebFunction
    - key: scheduled-function
      handler: src/backend/scheduled-func-name.forge.handleScheduledFunction

  webtrigger:
    - key: first-webtrigger
      function: web-function
    - key: second-webtrigger
      function: second-web-function

  scheduledTrigger:
    - key: scheduled-trigger
      function: scheduled-function
      interval: day

resources:
  - key: main
    path: src/frontend/dist

app:
  runtime:
    name: nodejs18.x
  id: ari:cloud:ecosystem::app/110ed4d0-3e25-4f98-93b0-b6d072f0a955

permissions:
  scopes:
    - storage:app
    - read:jira-work
```

- Direct File Reference: Each function is directly referenced by its file path (e.g., `src/backend/web-func-name.forge.handleWebFunction`), instead of consolidating the exports through a barrel file (index.ts).
- Harder to Maintain: This increases the risk of errors in the manifest file and makes the code harder to maintain, especially if file paths change.

**<green>Correct:</green>**

```yaml
# manifest.yml
modules:
  function:
    - key: web-function
      handler: index.handleWebFunction
    - key: second-web-function
      handler: index.handleSecondWebFunction
    - key: scheduled-function
      handler: index.handleScheduledFunction

  webtrigger:
    - key: first-webtrigger
      function: web-function
    - key: second-webtrigger
      function: second-web-function

  scheduledTrigger:
    - key: scheduled-trigger
      function: scheduled-function
      interval: day

resources:
  - key: main
    path: src/frontend/dist

app:
  runtime:
    name: nodejs18.x
  id: ari:cloud:ecosystem::app/110ed4d0-3e25-4f98-93b0-b6d072f0a955

permissions:
  scopes:
    - storage:app
    - read:jira-work
```

- The manifest includes only the functions and modules relevant to the examples: webtrigger, scheduledTrigger, and function.
- Function handlers point to the barrel file (src/backend/index.ts), aligning with the good folder architecture example.
- Frontend resources are referenced using path: src/frontend/dist.

## Module Amount Limitations

### Web Triggers

When using web triggers, it is possible to create a web trigger for each method for each endpoint you would like. For example, say you wanted an API for a user's behavior:

- `GET /users`
- `GET /users/{id}`
- `POST /users`
- `PUT /users/{id}`
- `DELETE /users/{id}`
<!-- eslint -->
- **<green>Do</green>** create one web trigger to handle all these routes.
- **<red>Avoid</red>** creating a web trigger for each route.
- **<green>Do</green>** create a separate web trigger for other endpoints, for example, `/posts`.

**<red>Incorrect:</red>**

<!-- Separate code blocks and add comments to make it more clear what is being done -->

```typescript
// src/backend/web-get-users.forge.ts
export async function getUsers(event: any): Promise<void> {
  if (event.method === "GET" && event.path === "/users") {
    console.log("Fetching all users");
  }
}
```

```typescript
// src/backend/web-get-user-by-id.forge.ts
export async function getUserById(event: any): Promise<void> {
  if (event.method === "GET" && event.path.startsWith("/users/")) {
    console.log(`Fetching user with ID: ${event.path.split("/").pop()}`);
  }
}
```

```typescript
// src/backend/web-post-users.forge.ts
export async function createUser(event: any): Promise<void> {
  if (event.method === "POST" && event.path === "/users") {
    console.log("Creating a new user");
  }
}
```

```typescript
// src/backend/web-put-users.forge.ts
export async function updateUser(event: any): Promise<void> {
  if (event.method === "PUT" && event.path.startsWith("/users/")) {
    console.log(`Updating user with ID: ${event.path.split("/").pop()}`);
  }
}
```

```typescript
// src/backend/web-delete-users.forge.ts
export async function deleteUser(event: any): Promise<void> {
  if (event.method === "DELETE" && event.path.startsWith("/users/")) {
    console.log(`Deleting user with ID: ${event.path.split("/").pop()}`);
  }
}
```

```yaml
# manifest.yml
modules:
  webtrigger:
    - key: get-users-trigger
      function: src/backend/get-users.forge.getUsers
    - key: get-user-by-id-trigger
      function: src/backend/get-user-by-id.forge.getUserById
    - key: post-users-trigger
      function: src/backend/post-users.forge.createUser
    - key: put-users-trigger
      function: src/backend/put-users.forge.updateUser
    - key: delete-users-trigger
      function: src/backend/delete-users.forge.deleteUser
```

- A separate web trigger is created for each individual route (GET, POST, PUT, DELETE), leading to unnecessary duplication and complexity.
- Managing multiple web triggers for closely related routes adds extra maintenance overhead.

**<green>Correct:</green>**

```typescript
// src/backend/web-users/web-users-get-all-users.ts
export async function getAllUsers(): Promise<void> {
  console.log("Fetching all users");
}
```

```typescript
// src/backend/web-users/web-users-get-user-by-id.ts
export async function getUserById(userId: string): Promise<void> {
  console.log(`Fetching user with ID: ${userId}`);
}
```

```typescript
// src/backend/web-users/web-users-create-user.ts
export async function createUser(): Promise<void> {
  console.log("Creating a new user");
}
```

```typescript
// src/backend/web-users/web-users-update-user.ts
export async function updateUser(userId: string): Promise<void> {
  console.log(`Updating user with ID: ${userId}`);
}
```

```typescript
// src/backend/web-users/web-users-delete-user.ts
export async function deleteUser(userId: string): Promise<void> {
  console.log(`Deleting user with ID: ${userId}`);
}
```

```typescript
// src/backend/web-users/web-users.forge.ts
import { getAllUsers } from "./web-users-get-all-users";
import { getUserById } from "./web-users-get-user-by-id";
import { createUser } from "./web-users-create-user";
import { updateUser } from "./web-users-update-user";
import { deleteUser } from "./web-users-delete-user";

export async function handleUsersApi(event: any): Promise<void> {
  if (!event.path.startsWith("/users")) {
    // Throw an error
    return;
  }

  const userId = event.path.split("/").pop();

  switch (event.method) {
    case "GET":
      if (userId) return getUserById(userId);
      return getAllUsers();

    case "POST":
      return createUser();

    case "PUT":
      return updateUser(userId);

    case "DELETE":
      return deleteUser(userId);

    default:
      console.log("Unhandled route or method");
      break;
  }
}
```

```yaml
# manifest.yml
modules:
  webtrigger:
    - key: users-api-trigger
      function: index.handleUsersApi
```

### Scheduled Triggers

Due to the limitations on the maximum number of scheduled triggers, you need to think differently. For instance, if you want to create two weekly scheduled triggers: a database cleaner and a reports generator.

- **<red>Avoid</red>** creating a scheduled trigger per feature.
- **<green>Do</green>** create scheduled triggers based on the interval.

**<red>Incorrect:</red>**

```ts
// src/backend/scheduled-database-cleaner.forge.ts
export async function cleanDatabase(): Promise<void> {
  console.log("Cleaning database...");
}
```

```ts
// src/backend/scheduled-reports-generator.forge.ts
export async function generateReports(): Promise<void> {
  console.log("Generating reports...");
}
```

```yaml
# manifest.yml
modules:
  scheduledTrigger:
    - key: database-cleaner-trigger
      function: index.cleanDatabase
      interval: week

    - key: reports-generator-trigger
      function: index.generateReports
      interval: week
```

- Each feature has its own scheduled trigger (database-cleaner and reports-generator), both running weekly.
- This approach wastes available scheduled triggers and does not consolidate tasks that could share the same interval.

**<green>Correct:</green>**

<!-- Add example with 2 scheduled triggers for different time increments -->

```ts
// src/backend/scheduled-database-cleaner.forge.ts
export async function cleanDatabase(): Promise<void> {
  console.log("Cleaning database...");
}
```

```ts
// src/backend/scheduled-reports-generator.forge.ts
export async function generateReports(): Promise<void> {
  console.log("Generating reports...");
}
```

```typescript
// src/backend/scheduled-weekly.ts
import { cleanDatabase } from "./database-cleaner";
import { generateReports } from "./reports-generator";

export async function handleWeeklyTasks(): Promise<void> {
  await generateReports();
  await cleanDatabase();
  console.log("Weekly tasks completed.");
}
```

```yaml
# manifest.yml
modules:
  scheduledTrigger:
    - key: weekly-tasks
      function: index.handleWeeklyTasks
      interval: week
```

- A single scheduled trigger, weekly-tasks-trigger, is created to handle all weekly tasks.
- This approach consolidates multiple tasks (cleanDatabase and generateReports) into a single scheduled trigger, optimizing the use of available triggers.
- Tasks are still modular and separated into their own files, but they are executed together by a single scheduled trigger based on the interval (week).

## Working With Teams

When doing a Forge deploy, it does not consider the code committed or pushed. It deploys the code that is in the file at the time of executing this command. To avoid confusion among team members working on the development branch, keep a dev branch for each member, for example, `dev-zishan` and `dev-joshua`.

- **<green>Do</green>** keep a separate development environment using the person’s name to help easily identify.
- **<red>Avoid</red>** working in the same environment on Forge.
- **<green>Do</green>** use a separate environment for each feature if you are on a large team working on multiple features at the same time.

## Deploying to Forge

- **<green>Do</green>** use CI/CD to automatically deploy code to development, staging, and production branches based on when pull requests are merged into these branches.
- **<green>Do</green>** set up restrictions to prevent direct pushes to these branches.
- **<red>Avoid</red>** pushing directly to development, staging, and production environments.

**<green>Correct:</green>**

```yaml
# bitbucket-pipelines.yml
pipelines:
  branches:
    development:
      - step:
          name: Deploy to Development
          caches:
            - node
          script:
            - npm install -g @forge/cli
            - forge login --non-interactive --email $FORGE_EMAIL --token $FORGE_API_TOKEN
            - forge deploy --environment development
          services:
            - docker

    staging:
      - step:
          name: Deploy to Staging
          caches:
            - node
          script:
            - npm install -g @forge/cli
            - forge login --non-interactive --email $FORGE_EMAIL --token $FORGE_API_TOKEN
            - forge deploy --environment staging
          services:
            - docker

    production:
      - step:
          name: Deploy to Production
          caches:
            - node
          script:
            - npm install -g @forge/cli
            - forge login --non-interactive --email $FORGE_EMAIL --token $FORGE_API_TOKEN
            - forge deploy --environment production
          services:
            - docker

definitions:
  caches:
    node: ~/.npm
```

## Security Measures

- **<red>Avoid</red>** hard-coding sensitive details. Use Forge Variables.

```bash
forge variables set MY_API_KEY "your-api-key-here"
```

- **<green>Do</green>** have authorization header checks on all web trigger handlers.

```typescript
export async function handleWebTrigger(event) {
  const authHeader = event.headers["Authorization"]?.[0];
  if (
    !authHeader ||
    authHeader !== `Bearer ${process.env.WEB_TRIGGER_AUTHORIZATION_HEADER}`
  ) {
    throw new Error("Unauthorized");
  }
  // proceed with logic
}
```

- **<green>Do</green>** validate input data to prevent injection attacks (e.g., SQL injection, NoSQL injection).

```typescript
import Joi from "joi";

export async function handleWebTrigger(event) {
  const { error } = schema.validate(JSON.parse(event.body));
  if (error) {
    throw new Error("Invalid data format");
  }
  // proceed with logic
}
```

- **<green>Do</green>** enforce strict CORS policies in web triggers.

```typescript
export async function handleWebTrigger(event) {
  const allowedOrigins = ["https://my-allowed-site.com"];
  const origin = event.headers["Origin"];

  if (!allowedOrigins.includes(origin)) {
    throw new Error("CORS policy violation");
  }
  // proceed with logic
}
```

- **<red>Avoid</red>** giving more permissions than your app requires. Use the principle of least privilege when specifying scopes in your `manifest.yml`.

```yaml
permissions:
  scopes:
    - read:jira-work
    - write:jira-work
```

- **<green>Do</green>** implement rate limiting on web triggers to mitigate Denial-of-Service (DoS) attacks.
- **<green>Do</green>** log important security-related events (e.g., failed authorization attempts) securely. Use logging libraries to track unusual activities, but ensure logs don’t contain sensitive information like passwords or API keys.

## UI Kit vs Custom UI

When building on the Forge platform, it is highly recommended to use the **UI Kit** whenever possible and only resort to **Custom UI** if absolutely necessary. The **UI Kit** simplifies development and helps maintain compatibility with Forge's environment.

If you do need to add Custom UI, try to use the **Frame** component to embed your Custom UI inside the UI Kit.

- **<green>Do</green>** use UI Kit whenever possible.
- **<green>Do</green>** use Custom UI when advanced styling or custom components are needed.
- **<green>Do</green>** use Frame component when possible to add custom UI to a UI Kit app.

### Benefits of UI Kit

- Easier to reload/tunnel during development.
- No need to recompile.
- Avoids complex hacks to get frameworks like Next.js to work with Forge.

### Tables In UI Kit

<!-- prettier-ignore-start -->
```jsx
import { DynamicTable } from '@forge/react';
import { head, rows } from './data';

export default function Table() {
  return <DynamicTable
            caption="List of US Presidents"
            head={head}
            rows={rows}
            rowsPerPage={5}
            isLoading={true}
            emptyView="No data to display"
            isRankable
            highlightedRowIndex={[0, 1]}
          />;
}
```
<!-- prettier-ignore-end -->

## Forge Storage Key-Value vs Entity Storage

When developing on the Forge platform, it's important to choose between **Forge Storage Key-Value** and **Forge Entity Storage** based on your specific needs. Each has its own strengths depending on the type of data and how you plan to access it.

- **<green>Do</green>** use **Entity Storage** when you need to index properties for querying purposes.
- **<green>Do</green>** use **Key-Value Storage**, whether it's storing strings or JSON, as long as you don't need to index properties.
- **<red>Avoid</red>** using **Entity Storage** if you don't need to index on properties, as there are limits on the number of entities that can exist.
- **<red>Avoid</red>** adding unnecessary indexes to prevent hitting storage limits.

### Benefits of Using the Correct Storage

- Efficiently manage storage by using Key-Value Storage for data that doesn’t require indexing.
- Prevent storage limitations by reserving Entity Storage for when indexing is essential.
- Maintain scalability by minimizing unnecessary use of indexed storage.

```ts
import { storage } from "@forge/api";

// Store user preferences
const userPreferences = {
  theme: "dark",
  notificationsEnabled: true,
};

// Set the user preferences in Key-Value Storage
await storage.set("user-123-preferences", userPreferences);

// Retrieve the user preferences from Key-Value Storage
const preferences = await storage.get("user-123-preferences");
console.log(preferences); // Output: { theme: 'dark', notificationsEnabled: true }
```

## Contact

If you have any feedback, questions, or ideas regarding this style guide, feel free to reach out via email. We'd love to hear from you! [forge@valiantys.com](mailto:forge@valiantys.com)
