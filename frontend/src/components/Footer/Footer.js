import { Layout } from "antd";
const { Footer } = Layout;

const AppFooter = () => {
  return (
    <Footer style={{ textAlign: "center" }}>
      <span>Nordigen API Demo by</span>{" "}
      <a href="mailto:acidpictures@gmail.com">acidpictures@gmail.com</a>
    </Footer>
  );
};

export default AppFooter;
