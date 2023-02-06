import axios from "axios";

export const BACKEND_URL =
  process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
// axios.defaults.baseURL =
//   process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

export async function fetchInstitutions() {
  return await axios.get(`/api/institutions`);
}

export async function fetchAccounts() {
  return await axios.get(`/api/accounts`);
}

export async function fetchTransactions(accountId) {
  return await axios.get(
    accountId ? `/api/transactions/${accountId}` : `/api/latest_transactions`
  );
}
