import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import FormChildren from "./FormChildren";
import "../Style/InsertForm.css";

// function required() {
//   const houseType = document.getElementById("houseType").value;
//   const houseOwner = document.getElementById("houseOwner").value;
//   const housePrice = document.getElementById("housePrice").value;
//   const houseAddress = document.getElementById("houseAddress").value;
//   const houseOwnership = document.getElementById("houseOwnership").value;

//   if (
//     houseType === "" ||
//     houseOwner === "" ||
//     housePrice === "" ||
//     houseAddress === "" ||
//     houseOwnership === ""
//   ) {
//     if (houseType === "") {
//       const inputField = document.getElementById("houseType");
//       inputField.style.border = "1px solid #fd7676";
//     }
//     if (houseOwner === "") {
//       const inputField = document.getElementById("houseOwner");
//       inputField.style.border = "1px solid #fd7676";
//     }
//     if (housePrice === "") {
//       const inputField = document.getElementById("housePrice");
//       inputField.style.border = "1px solid #fd7676";
//     }
//     if (houseAddress === "") {
//       const inputField = document.getElementById("houseAddress");
//       inputField.style.border = "1px solid #fd7676";
//     }
//     if (houseOwnership === "") {
//       const inputField = document.getElementById("houseOwnership");
//       inputField.style.border = "1px solid #fd7676";
//     }
//     let para = document.createElement("div");
//     para.className = "alert alert-danger";
//     para.id = "alertChild";
//     const node = document.createTextNode(
//       "Please enter all the mandatory fields (*)"
//     );
//     para.appendChild(node);

//     let para2 = document.createElement("a");
//     para2.href = "#";
//     para2.className = "close";
//     para2.id = "closeBtn";
//     para2.onclick = cancelAlert;
//     para2.innerHTML = "&times;";

//     const element = document.getElementById("alert");
//     para.appendChild(para2);
//     element.appendChild(para);
//     return false;
//   }
//   return true;
// }
// function cancelAlert() {
//   const element2 = document.getElementById("closeBtn");
//   element2.remove();
//   const element = document.getElementById("alertChild");
//   element.remove();
// }

const resetForm = () => {
  document.getElementById("insertForm").reset();
};
const InsertData = () => {
  const [houseType, sethouseType] = useState("");
  const [houseOwner, sethouseOwner] = useState("");
  const [housePrice, sethousePrice] = useState("");
  const [houseAddress, sethouseAddress] = useState("");
  const [houseOwnership, sethouseOwnership] = useState("");
  const handleSubmit = () => {
    console.log("form submitted ✅");
    console.log(
      this.houseType,
      this.houseOwner,
      this.housePrice,
      this.houseAddress,
      this.houseOwnership
    );
  };

  return (
    <div>
      <div id="alert"></div>
      <div className="d-flex align-items-center py-5">
        <div className="container">
          <div className="row">
            <Form id="insertForm">
              <div className="mx-auto">
                <h3 className="mb-3">Nhập dữ liệu</h3>

                <FormChildren
                  header="Loại hình"
                  example="Ví dụ: Chung cư"
                  idname="houseType"
                  value={houseType}
                  changeValue={sethouseType}
                ></FormChildren>
                <FormChildren
                  header="Chủ sở hữu"
                  example="Tên người sở hữu"
                  idname="houseOwner"
                  value={houseOwner}
                  changeValue={sethouseOwner}
                ></FormChildren>
                <FormChildren
                  header="Giá tiền"
                  example="1 tỷ 400 triệu"
                  idname="housePrice"
                  value={housePrice}
                  changeValue={sethousePrice}
                ></FormChildren>
                <FormChildren
                  header="Địa chỉ"
                  example="Địa chỉ"
                  idname="houseAddress"
                  value={houseAddress}
                  changeValue={sethouseAddress}
                ></FormChildren>
                <FormChildren
                  header="Chứng nhận sở hữu"
                  example="Sổ hồng"
                  idname="houseOwnership"
                  value={houseOwnership}
                  changeValue={sethouseOwnership}
                ></FormChildren>
                <div>
                  <button
                    className="btn btn-primary btn-sm fw-bold"
                    type=" button"
                    onClick={() => handleSubmit()}
                  >
                    Thêm thông tin
                  </button>
                  <button
                    className="btn btn-secondary btn-sm fw-bold"
                    type=" button"
                    onClick={() => resetForm()}
                  >
                    Hủy
                  </button>
                </div>
              </div>
            </Form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InsertData;
