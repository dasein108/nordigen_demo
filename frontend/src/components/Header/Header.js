import React from "react";

import { Layout, Space, Button, Spin, Dropdown } from "antd";
import { BankOutlined } from "@ant-design/icons";
import { useQuery } from "react-query";
import { fetchInstitutions, BACKEND_URL } from "../../services";
import ErrorBox from "../ErrorBox/ErrorBox";
const { Header } = Layout;

const mapMenuProps = (data) => ({
  label: <a href={`${BACKEND_URL}/api/connect/${data.id}`}>{data.name}</a>,
  key: data.id,
  icon: <img src={data.logo} alt={data.name} width="32px" />,
});

const AppHeader = () => {
  const { data, status, isFetching } = useQuery(
    "institutions",
    fetchInstitutions
  );

  return (
    <>
      <Header>
        <Space wrap>
          {isFetching && <Spin />}
          {status === "error" && <ErrorBox />}
          {status === "success" && (
            <Dropdown
              menu={{ items: data.data.results.map((i) => mapMenuProps(i)) }}
            >
              <Button>
                <Space>
                  <BankOutlined />
                  Connect Bank
                </Space>
              </Button>
            </Dropdown>
          )}
        </Space>
      </Header>
    </>
  );
};

export default AppHeader;
