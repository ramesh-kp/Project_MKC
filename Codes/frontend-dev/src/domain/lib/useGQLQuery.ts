/* eslint-disable no-undef */
import { GraphQLClient } from "graphql-request";

const endpoint = process.env.NEXT_PUBLIC_API_URL || "";

const graphQLClient = (headers?: HeadersInit) =>
  new GraphQLClient(endpoint, { credentials: "include", headers: {...headers, Accept: "application/json"} });
export default graphQLClient;

