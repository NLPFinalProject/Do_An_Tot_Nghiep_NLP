import { Component, OnInit, Input } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@../../../src/app/login/user-authenticate-service';
import moment from 'moment';
import { NzNotificationService } from 'ng-zorro-antd/notification';
@Component({
  selector: 'app-profile-user',
  templateUrl: './profile-user.component.html',
  styleUrls: ['./profile-user.component.scss'],
})
export class ProfileUserComponent implements OnInit {
  validateForm: FormGroup;
  dateFormat = 'dd/MM/yyyy';
  @Input() data: any;
  //@Input() userdata:any
  constructor(
    private fb: FormBuilder,
    private router: Router,
    private userService: UserService,
    private notification: NzNotificationService
  ) {
    console.log(this.data);
    //console.log(this.userdata);
  }

  submitForm(): void {
    // tslint:disable-next-line:forin
    console.log(this.validateForm);
    console.log(this.validateForm.value);
    var data = {
      email: this.validateForm.value.email,
      emailOrganization: this.validateForm.value.emailOrganization,
      organization: this.validateForm.value.organization,
      fullName: this.validateForm.value.fullName,

      password: this.validateForm.value.password,

      phoneNumber: this.validateForm.value.phoneNumber,

      ngaySinh: this.validateForm.value.ngaySinh,
      gioiTinh: this.validateForm.value.gioiTinh,
      //captcha: [null, [Validators.required]],
    };
    //console.log(data);
    for (const i in this.validateForm.controls) {
      this.validateForm.controls[i].markAsDirty();
      this.validateForm.controls[i].updateValueAndValidity();
    }
    console.log('data is');
    console.log(data);
    this.userService.updateUSer(data).subscribe(
      (data) => {
        console.log('sucess');
        this.notification.success('Thành công', 'Cập nhật thông tin thành công');
        //     this.showErrorNotification(`${MessageConstant.LoginFailed}`);
      },
      (error) => {
        console.log('Lỗi người dùng');
        this.notification.error('Thất bại', 'Cập nhật thông tin thất bại');
      }
    );
  }
  /*updateUserData() {
    this.submitForm();
  }*/
  Clicked() {
    console.log('yeah here I clicked');
    this.router.navigate(['reset-password'], { replaceUrl: true });
  }
  updateConfirmValidator(): void {
    /** wait for refresh value */
    Promise.resolve().then(() => this.validateForm.controls.checkPassword.updateValueAndValidity());
  }
  ngOnChanges() {
    console.log(this.data.DateOfBirth);
    let momentVariable = moment(this.data.DateOfBirth, 'MM-DD-YYYY');
    let newDate = momentVariable.format('YYYY-MM-DD');
    console.log(this.data);
    this.validateForm = this.fb.group({
      email: [this.data.username, [Validators.email, Validators.required]],
      phoneNumber: [this.data.phone, [Validators.required]],
      emailOrganization: [this.data.EmailOrganization, [Validators.email]],
      phoneOrganization: [this.data.phonelOrganization],
      fullName: [this.data.name, [Validators.required]],
      ngaySinh: [this.data.DateOfBirth, [Validators.required]],
    });
  }
  confirmationValidator = (control: FormControl): { [s: string]: boolean } => {
    if (!control.value) {
      return { required: true };
    } else if (control.value !== this.validateForm.controls.password.value) {
      return { confirm: true, error: true };
    }
  };

  getCaptcha(e: MouseEvent): void {
    e.preventDefault();
  }

  ngOnInit(): void {
    if (this.data != undefined) {
      console.log(this.data.DateOfBirth);
      let momentVariable = moment(this.data.DateOfBirth, 'MM-DD-YYYY');
      let newDate = momentVariable.format('YYYY-MM-DD');
      console.log(this.data);
      this.validateForm = this.fb.group({
        email: [this.data.username, [Validators.email, Validators.required]],
        phoneNumber: [this.data.phone, [Validators.required]],
        emailOrganization: [this.data.EmailOrganization, [Validators.email]],
        phoneOrganization: [this.data.phonelOrganization],
        fullName: [this.data.name, [Validators.required]],
        ngaySinh: [this.data.DateOfBirth, [Validators.required]],
      });
    } else {
      this.validateForm = this.fb.group({
        email: ['', [Validators.email, Validators.required]],
        phoneNumber: ['', [Validators.required]],
        emailOrganization: ['', [Validators.required]],
        website: ['', [Validators.required]],
        phoneOrganization: [''],
        fullName: ['', [Validators.required]],
        ngaySinh: ['', [Validators.required]],
      });
    }
  }
}
