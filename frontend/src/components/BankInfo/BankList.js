import React from "react";

import { Space, Spin } from "antd";
import { useQuery } from "react-query";
import ErrorBox from "../ErrorBox/ErrorBox";
import BankInfo from "./BankInfo";
import { fetchAccounts } from "../../services";

const BankList = () => {
  const { data, status, isFetching } = useQuery("accounts", fetchAccounts);

  return (
    <Space wrap>
      {isFetching && <Spin />}
      {status === "error" && <ErrorBox />}
      {status === "success" && (
        <>
          {data.data.results.map((item) => (
            <BankInfo key={`account_${item.account_id}`} data={item} />
          ))}
        </>
      )}
    </Space>
  );
};

export default BankList;
