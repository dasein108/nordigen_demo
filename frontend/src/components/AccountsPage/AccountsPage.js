import React, { useState, useEffect } from "react";

import { Layout, Space, Button, Spin, Dropdown, Result } from "antd";

import BankList from "../BankInfo/BankList";
import AccountTransactions from "../AccountTransactions/AccountTransactions";

const AccountsPage = () => {
  return (
    <Space direction="vertical">
      <h3>Banks</h3>
      <BankList />
      <h3>Latest Transactions</h3>
      <AccountTransactions />
    </Space>
  );
};

export default AccountsPage;
