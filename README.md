# Forge Style Guide

**Last reviewed:** September 10, 2026. Examples target the Forge Node.js 24 runtime and UI Kit 10 or later.

[View the published Forge Style Guide](https://www.valiantys.com/en/resources/forge-style-guide)

This guide captures practical conventions from Valiantys engineers building enterprise applications on Atlassian Forge. It is a living reference that evolves with the platform and community feedback.

## Purpose

The guide provides opinionated defaults for structuring, securing, and operating Forge applications. Treat each recommendation as a starting point and document exceptions that better fit your application.

## Community Contributions

Corrections, current examples, and well-supported alternative approaches are welcome. Recommendations should link to primary documentation when they depend on platform behavior or limits.

[Read the contribution guide to propose an improvement on GitHub.](./CONTRIBUTING.md)

## Maintainers

- **Zishan Aslam**, Software Architect
- **Zachary Kipping**, R&D Manager
- **Alisha Robinson**, Software Engineer and Forge Instructor

## Table of Contents

- [Single Purpose Code](#single-purpose-code)
- [Folder Architecture](#folder-architecture)
- [Manifest File Pointers](#manifest-file-pointers)
- [Module Amount Limitations](#module-amount-limitations)
- [Working With Teams](#working-with-teams)
- [Deploying to Forge](#deploying-to-forge)
- [Code Optimizations](#code-optimizations)
- [Security Measures](#security-measures)
- [UI Kit vs Custom UI](#ui-kit-vs-custom-ui)
- [Forge Storage: Key Value vs Entity](#forge-storage-key-value-vs-entity-storage)
- [Contact Us / Feedback](#contact)

## Single Purpose Code

Keep each file focused on one cohesive responsibility. Split unrelated behavior, but keep small helpers and components together when separation would make the code harder to follow.

- **Do:** group code that changes for the same reason.
- **Do:** split a function or component when it has an independent owner, lifecycle, or test boundary.
- **Avoid:** creating one-line files that only re-export, cast, or wrap another function.

### Single Function Per File

**Incorrect:**

```typescript
// src/triggers/web/multi-functions.ts
export async function handleWebTrigger(event: WebTriggerRequest): Promise<void> {
  console.log("Handling web trigger:", event);
}

export async function handleSecondWebTrigger(event: WebTriggerRequest): Promise<void> {
  console.log("Handling second web trigger:", event);
}
```

This example mixes two unrelated trigger handlers in one file.

**Correct:**

```typescript
// src/triggers/web/handleWebTrigger.ts
export async function handleWebTrigger(event: WebTriggerRequest): Promise<void> {
  console.log("Handling web trigger:", event);
}
```

```typescript
// src/triggers/web/handleSecondWebTrigger.ts
export async function handleSecondWebTrigger(event: WebTriggerRequest): Promise<void> {
  console.log("Handling second web trigger:", event);
}
```

Each independently deployed handler has a clear home.

### Single Component Per File

**Incorrect:**

```typescript
// src/components/MultiComponents.tsx
import { Button, Text } from "@forge/react";

const MyButton = () => {
  return (
    <Button onClick={() => console.log("Button clicked!")}>Click me</Button>
  );
};

const MyText = () => {
  return <Text content="Hello, World!" />;
};
```

This file combines unrelated UI elements without a shared responsibility.

**Correct:**

```typescript
// src/components/MyButton.tsx
import { Button } from "@forge/react";

const MyButton = () => {
  return (
    <Button onClick={() => console.log("Button clicked!")}>Click me</Button>
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

Each independently reused component has a clear module boundary.

## Folder Architecture

Having each function/component separate per file can create a lot of files, so you need to maintain a good and easy-to-understand folder architecture. This architecture should ideally tell you exactly what is inside that folder without you even needing to open it. Keep backend code inside a folder marked as `src/backend` and the frontend code in `src/frontend`.

- **Do:** keep all Forge functions in a file suffixed with `.forge.ts` such as `filename.forge.ts`.
- **Do:** keep all code within the `src` folder.
- **Do:** keep all backend code inside a `src/backend` folder and all frontend code in `src/frontend`.
- **Do:** keep each file name prefixed with the forge module.
  - src/backend/web-func-name.forge.ts
  - src/backend/web-2nd-func-name.forge.ts
  - src/backend/scheduled-func-name.forge.ts

**Incorrect:**

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

**Correct:**

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

This separates backend and frontend code into distinct folders (src/backend and src/frontend) and uses clear file naming conventions with the `.forge.ts` suffix and module prefixes (web-, scheduled-). This structure is immediately intuitive and makes it easier to understand the contents of each folder.

## Manifest File Pointers

In the manifest file, you often need to specify a path to a function in your code. To avoid typos in the path, it is cleaner and easier to have everything exported in your index file. This way, your manifest file can always use the index file as the path.

Reference: [Forge runtimes and manifest configuration](https://developer.atlassian.com/platform/forge/function-reference/nodejs-runtime/).

- **Do:** use the index file as the source of all functions in your manifest file.
- **Do:** export all code that the manifest file needs in your index file.

### Barrel File Exports

**Incorrect:**

```typescript
// src/backend/web-func-name.forge.ts
export async function handleWebFunction(event: WebTriggerRequest): Promise<void> {
  console.log("Handling web trigger:", event);
}
```

```typescript
// src/backend/web-2nd-func-name.forge.ts
export async function handleSecondWebFunction(event: WebTriggerRequest): Promise<void> {
  console.log("Handling second web trigger:", event);
}
```

```typescript
// src/backend/scheduled-func-name.forge.ts
export async function handleScheduledFunction(_event: unknown): Promise<void> {
  console.log("Handling scheduled trigger:", _event);
}
```

**Correct:**

```typescript
// src/backend/web-func-name.forge.ts
export async function handleWebFunction(event: WebTriggerRequest): Promise<void> {
  console.log("Handling web trigger:", event);
}
```

```typescript
// src/backend/web-2nd-func-name.forge.ts
export async function handleSecondWebFunction(event: WebTriggerRequest): Promise<void> {
  console.log("Handling second web trigger:", event);
}
```

```typescript
// src/backend/scheduled-func-name.forge.ts
export async function handleScheduledFunction(_event: unknown): Promise<void> {
  console.log("Handling scheduled trigger:", _event);
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

**Incorrect:**

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
    name: nodejs24.x
  id: ari:cloud:ecosystem::app/110ed4d0-3e25-4f98-93b0-b6d072f0a955

permissions:
  scopes:
    - storage:app
    - read:jira-work
```

- Direct File Reference: Each function is directly referenced by its file path (e.g., `src/backend/web-func-name.forge.handleWebFunction`), instead of consolidating the exports through a barrel file (index.ts).
- Harder to Maintain: This increases the risk of errors in the manifest file and makes the code harder to maintain, especially if file paths change.

**Correct:**

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
    name: nodejs24.x
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

Forge does not authenticate web-trigger URLs. Each handler must authenticate requests using the security scheme supported by its caller. Reference: [Forge web triggers](https://developer.atlassian.com/platform/forge/runtime-reference/web-trigger/).

- `GET /users`
- `GET /users/{id}`
- `POST /users`
- `PUT /users/{id}`
- `DELETE /users/{id}`
- **Do:** create one web trigger to handle all these routes.
- **Avoid:** creating a web trigger for each route.
- **Do:** create a separate web trigger for other endpoints, for example, `/posts`.

**Incorrect:**

```typescript
// src/backend/web-get-users.forge.ts
export async function getUsers(event: WebTriggerRequest): Promise<void> {
  if (event.method === "GET" && event.path === "/users") {
    console.log("Fetching all users");
  }
}
```

```typescript
// src/backend/web-get-user-by-id.forge.ts
export async function getUserById(event: WebTriggerRequest): Promise<void> {
  if (event.method === "GET" && event.path.startsWith("/users/")) {
    console.log(`Fetching user with ID: ${event.path.split("/").pop()}`);
  }
}
```

```typescript
// src/backend/web-post-users.forge.ts
export async function createUser(event: WebTriggerRequest): Promise<void> {
  if (event.method === "POST" && event.path === "/users") {
    console.log("Creating a new user");
  }
}
```

```typescript
// src/backend/web-put-users.forge.ts
export async function updateUser(event: WebTriggerRequest): Promise<void> {
  if (event.method === "PUT" && event.path.startsWith("/users/")) {
    console.log(`Updating user with ID: ${event.path.split("/").pop()}`);
  }
}
```

```typescript
// src/backend/web-delete-users.forge.ts
export async function deleteUser(event: WebTriggerRequest): Promise<void> {
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

**Correct:**

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
export async function createUser(body: string): Promise<void> {
  console.log("Creating a new user");
}
```

```typescript
// src/backend/web-users/web-users-update-user.ts
export async function updateUser(userId: string, body: string): Promise<void> {
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

export async function handleUsersApi(event: WebTriggerRequest): Promise<void> {
  const path = event.queryParameters?.path?.join("") ?? "";

  if (!path.startsWith("users")) {
    throw new Error("Unknown route");
  }

  const userId = path.includes("/") ? path.split("/").pop() : undefined;

  switch (event.method) {
    case "GET":
      if (userId) return getUserById(userId);
      return getAllUsers();

    case "POST":
      return createUser(event.body);

    case "PUT":
      if (!userId) throw new Error("User ID is required");
      return updateUser(userId, event.body);

    case "DELETE":
      if (!userId) throw new Error("User ID is required");
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

- **Avoid:** creating a scheduled trigger per feature.
- **Do:** create scheduled triggers based on the interval.

**Incorrect:**

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

**Correct:**

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

Forge deploys the files in the current working tree, including uncommitted changes. Give each developer or feature an isolated Forge environment so one person cannot accidentally deploy another person’s work.

- **Do:** keep a separate development environment using the person’s name to help easily identify.
- **Avoid:** working in the same environment on Forge.
- **Do:** use a separate environment for each feature if you are on a large team working on multiple features at the same time.

## Deploying to Forge

- **Do:** use CI/CD to automatically deploy code to development, staging, and production branches based on when pull requests are merged into these branches.
- **Do:** set up restrictions to prevent direct pushes to these branches.
- **Avoid:** pushing directly to development, staging, and production environments.

**Correct:**

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

## Code Optimizations

- **Do:** parse and validate the payload schema first, and return early on failure.
- **Do:** perform header and authorization checks only after the schema check passes.
- **Avoid:** reading from storage or calling external services before you know the payload is well-formed.
- **Avoid:** trusting unvalidated fields for anything beyond the structural check itself; schema validation is not a substitute for authorization.

Order the checks inside a web trigger (or any other event handler) so the cheapest checks run first. Payload schema validation only inspects the shape of the payload already in memory and costs nothing extra. Authorization and authentication often require a storage read or an external call, for example, comparing a token against a secret stored in Forge storage. If you check authorization first, every request, including garbage payloads and bots probing the URL, pays for a Forge runtime invocation and a storage read before it is rejected. If you validate the schema first, malformed requests are rejected with a local check and never reach the storage read, so cost tracks genuinely well-formed traffic.

**Incorrect:**

```typescript
import Joi from "joi";
import { kvs } from "@forge/kvs";

const schema = Joi.object({
  username: Joi.string().alphanum().min(3).max(30).required(),
});

export async function handleWebTrigger(event: WebTriggerRequest) {
  const authHeader = event.headers.authorization?.[0];
  const storedToken = await kvs.get("web-trigger-token"); // storage read on every request

  if (!authHeader || authHeader !== `Bearer ${storedToken}`) {
    return { statusCode: 401, headers: {}, body: "Unauthorized" };
  }

  let body: unknown;
  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, headers: {}, body: "Invalid JSON" };
  }

  const { error } = schema.validate(body);
  if (error) {
    return { statusCode: 400, headers: {}, body: "Invalid data format" };
  }

  return { statusCode: 204, headers: {}, body: "" };
}
```

A malformed or unauthorized request still triggers a storage read to fetch the stored token before it is rejected, so cost scales with all incoming traffic rather than just valid requests.

**Correct:**

```typescript
import Joi from "joi";
import { kvs } from "@forge/kvs";

const schema = Joi.object({
  username: Joi.string().alphanum().min(3).max(30).required(),
});

export async function handleWebTrigger(event: WebTriggerRequest) {
  let body: unknown;
  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, headers: {}, body: "Invalid JSON" };
  }

  const { error } = schema.validate(body);
  if (error) {
    return { statusCode: 400, headers: {}, body: "Invalid data format" };
  }

  const authHeader = event.headers.authorization?.[0];
  const storedToken = await kvs.get("web-trigger-token"); // only read once the payload is well-formed

  if (!authHeader || authHeader !== `Bearer ${storedToken}`) {
    return { statusCode: 401, headers: {}, body: "Unauthorized" };
  }

  return { statusCode: 204, headers: {}, body: "" };
}
```

Malformed payloads are rejected by a local, in-memory schema check before any storage is read, so you only pay for a storage read once a request is at least well-formed.

## Security Measures

- **Avoid:** hard-coding sensitive details. Use Forge Variables.
- **Do:** use encrypted Forge environment variables

```bash
forge variables set MY_API_KEY "your-api-key-here"
# Encrypted variables
forge variables set MY_API_KEY "your-api-key-here" --encrypt
```

- **Do:** authenticate every web trigger using the scheme supported by its caller, such as an HMAC signature or bearer token. Forge web-trigger URLs are not authenticated by the platform. 

See [Code Optimizations](#code-optimizations) for why this check should run after schema validation, not before.

```typescript
export async function handleWebTrigger(event: WebTriggerRequest) {
  const authHeader = event.headers.authorization?.[0];
  if (
    !authHeader ||
    authHeader !== `Bearer ${process.env.WEB_TRIGGER_AUTHORIZATION_HEADER}`
  ) {
    return { statusCode: 401, headers: {}, body: "Unauthorized" };
  }

  return { statusCode: 204, headers: {}, body: "" };
}
```

- **Do:** validate input data to handle invalid data.

```typescript
import Joi from "joi";

// This is just an example, please feel free to use any preferred library for your team.
const schema = Joi.object({
    username: Joi.string()
        .alphanum()
        .min(3)
        .max(30)
        .required()
});


export async function handleWebTrigger(event: WebTriggerRequest) {
  let body: unknown;

  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, headers: {}, body: "Invalid JSON" };
  }

  const { error } = schema.validate(body);
  if (error) {
    return { statusCode: 400, headers: {}, body: "Invalid data format" };
  }

  return { statusCode: 204, headers: {}, body: "" };
}
```

- **Do:** enforce strict CORS policies in web triggers.

```typescript
export async function handleWebTrigger(event: WebTriggerRequest) {
  const allowedOrigins = ["https://my-allowed-site.com"];
  const origin = event.headers.origin?.[0];

  if (!origin || !allowedOrigins.includes(origin)) {
    return { statusCode: 403, headers: {}, body: "Origin not allowed" };
  }

  return {
    statusCode: 204,
    headers: { "Access-Control-Allow-Origin": [origin] },
    body: "",
  };
}
```

- **Avoid:** giving more permissions than your app requires. Use the principle of least privilege when specifying scopes in your `manifest.yml`.

```yaml
permissions:
  scopes:
    - read:jira-work
    - write:jira-work
```

- **Do:** validate input data to prevent injection attacks (e.g., SQL injection, NoSQL injection).
- **Do:** implement rate limiting on web triggers to mitigate Denial-of-Service (DoS) attacks.
- **Do:** log important security-related events (e.g., failed authorization attempts) securely. Use logging libraries to track unusual activities, but ensure logs don’t contain sensitive information like passwords or API keys.

## UI Kit vs Custom UI

When building on the Forge platform, it is highly recommended to use the **UI Kit** whenever possible and only resort to **Custom UI** if absolutely necessary. The **UI Kit** simplifies development and helps maintain compatibility with Forge's environment.

If you do need to add Custom UI, try to use the **Frame** component to embed your Custom UI inside the UI Kit.

Reference: [Forge UI Kit components](https://developer.atlassian.com/platform/forge/ui-kit/components/) and the [Frame component](https://developer.atlassian.com/platform/forge/ui-kit/components/frame/).

- **Do:** use UI Kit whenever possible.
- **Do:** use Custom UI when advanced styling or custom components are needed.
- **Do:** use Frame component when possible to add custom UI to a UI Kit app.

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
            isLoading={false}
            emptyView="No data to display"
            isRankable
            highlightedRowIndex={[0, 1]}
          />;
}
```
<!-- prettier-ignore-end -->

## Forge Storage Key-Value vs Entity Storage

When developing on the Forge platform, it's important to choose between **Forge Storage Key-Value** and **Forge Entity Storage** based on your specific needs. Each has its own strengths depending on the type of data and how you plan to access it.

Reference: [Forge Custom Entity Store](https://developer.atlassian.com/platform/forge/storage-reference/entities-api/) and [platform limits](https://developer.atlassian.com/platform/forge/platform-quotas-and-limits/).

- **Do:** use **Entity Storage** when you need to index properties for querying purposes.
- **Do:** use **Key-Value Storage**, whether it's storing strings or JSON, as long as you don't need to index properties.
- **Avoid:** using **Entity Storage** if you don't need to index on properties, as there are limits on the number of entities that can exist.
- **Avoid:** adding unnecessary indexes to prevent hitting storage limits.

### Benefits of Using the Correct Storage

- Efficiently manage storage by using Key-Value Storage for data that doesn’t require indexing.
- Prevent storage limitations by reserving Entity Storage for when indexing is essential.
- Maintain scalability by minimizing unnecessary use of indexed storage.

```ts
import { kvs } from "@forge/kvs";

// Store user preferences
const userPreferences = {
  theme: "dark",
  notificationsEnabled: true,
};

// Set the user preferences in Key-Value Storage
await kvs.set("user-123-preferences", userPreferences);

// Retrieve the user preferences from Key-Value Storage
const preferences = await kvs.get("user-123-preferences");
console.log(preferences); // Output: { theme: 'dark', notificationsEnabled: true }
```

## Contact

If you have feedback, questions, or ideas about this guide, contact [Alisha Robinson](mailto:alisha.robinson@valiantys.com) at [alisha.robinson@valiantys.com](mailto:alisha.robinson@valiantys.com).
