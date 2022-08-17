import React, { useState } from "react";
import Form from 'react-bootstrap/Form';
import FormChildren from "./FormChildren";
import "../Style/InsertForm.css";

const resetForm = () => {
    document.getElementById("insertForm").reset();
    console.log("ok");
}
const InsertData = () => {
    const [houseType, sethouseType] = useState('');
    const [houseOwner, sethouseOwner] = useState('');
    const [housePrice, sethousePrice] = useState('');
    const [houseAddress, sethouseAddress] = useState('');
    const [houseOwnership, sethouseOwnership] = useState('');
    const handleSubmit = () => {
        console.log('form submitted ✅');
        console.log(this.houseType, this.houseOwner, this.housePrice, this.houseAddress, this.houseOwnership);
    };

    return (
        <div>
            <div className="login d-flex align-items-center py-5">
                <div className="container">
                    <div className="row">
                        <Form id="insertForm">
                            <div className="mx-auto">
                                <h3 className="mb-3">Nhập dữ liệu</h3>

                                <FormChildren header="Loại hình" example="Ví dụ: Chung cư" idname="houseType" value={houseType} changeValue={sethouseType}></FormChildren>
                                <FormChildren header="Chủ sở hữu" example="Tên người sở hữu" idname="houseOwner" value={houseOwner} changeValue={sethouseOwner}></FormChildren>
                                <FormChildren header="Giá tiền" example="1 tỷ 400 triệu" idname="housePrice" value={housePrice} changeValue={sethousePrice}></FormChildren>
                                <FormChildren header="Địa chỉ" example="Địa chỉ" idname="houseAddress" value={houseAddress} changeValue={sethouseAddress}></FormChildren>
                                <FormChildren header="Chứng nhận sở hữu" example="Sổ hồng" idname="houseOwnership" value={houseOwnership} changeValue={sethouseOwnership}></FormChildren>
                                <div>
                                    <button className="btn btn-primary btn-sm fw-bold" type=" button" onClick={() => handleSubmit()}>Thêm thông tin</button>
                                    <button className="btn btn-secondary btn-sm fw-bold" type=" button" onClick={() => resetForm()}>Hủy</button>
                                </div>
                            </div>
                        </Form>
                    </div>
                </div >
            </div >
        </div >
    );
}

export default InsertData;