import "./App.css";

import { Layout } from "antd";
import { QueryClient, QueryClientProvider } from "react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AppHeader from "./Header/Header";
import AppFooter from "./Footer/Footer";
import AccountsPage from "./AccountsPage/AccountsPage";
import TransactionsPage from "./TransactionsPage/TransactionsPage";
const { Content } = Layout;

const staleTime = 1000 * 5;

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      refetchOnmount: false,
      refetchOnReconnect: false,
      retry: false,
      staleTime,
    },
  },
});

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <QueryClientProvider client={queryClient}>
          <Layout>
            <AppHeader />
            <Content>
              <Routes>
                <Route index element={<AccountsPage />} />
                <Route
                  path="transactions/:accountId"
                  element={<TransactionsPage />}
                />
              </Routes>
            </Content>
            <AppFooter />
          </Layout>
        </QueryClientProvider>
      </div>
    </BrowserRouter>
  );
}

export default App;
