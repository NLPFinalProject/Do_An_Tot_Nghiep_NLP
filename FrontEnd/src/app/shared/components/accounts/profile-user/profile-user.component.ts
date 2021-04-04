import { Component, OnInit, Input } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '@../../../src/app/login/user-authenticate-service';
@Component({
  selector: 'app-profile-user',
  templateUrl: './profile-user.component.html',
  styleUrls: ['./profile-user.component.scss']
})
export class ProfileUserComponent implements OnInit {
  validateForm: FormGroup;

  @Input() data: any;
  //@Input() userdata:any
  constructor(private fb: FormBuilder, private router: Router,private userServive:UserService) {
    console.log(this.data);
    //console.log(this.userdata);
  }

  submitForm(): void {
    // tslint:disable-next-line:forin
    console.log(this.validateForm)
    console.log(this.validateForm.value);
    var data = {
      email: this.validateForm.value.email,
      emailOrganization: this.validateForm.value.emailOrganization,
      organization: this.validateForm.value.organization,
      fullName: this.validateForm.value.fullName,
     
      password: this.validateForm.value.password,

      phoneNumber: this.validateForm.value.phoneNumber,

      ngaySinh: this.validateForm.value.ngaySinh,
      gioiTinh: this.validateForm.value.gioiTinh
      //captcha: [null, [Validators.required]],
    };
    //console.log(data);
    for (const i in this.validateForm.controls) {
      this.validateForm.controls[i].markAsDirty();
      this.validateForm.controls[i].updateValueAndValidity();
    }
    console.log('data is');
    console.log(data);
    this.userServive.updateUSer(data).subscribe(
      (data)=>{
        console.log('sucess');
      }
    )
  }

  updateConfirmValidator(): void {
    /** wait for refresh value */
    Promise.resolve().then(() => this.validateForm.controls.checkPassword.updateValueAndValidity());
  }

  confirmationValidator = (control: FormControl): { [s: string]: boolean } => {
    if (!control.value) {
      return { required: true };
    } else if (control.value !== this.validateForm.controls.password.value) {
      return { confirm: true, error: true };
    }
  };
  updateUserData()
  {

  }
  getCaptcha(e: MouseEvent): void {
    e.preventDefault();
  }

  ngOnInit(): void {
    if (this.data != undefined) {
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
        email: ['acb@gmail.com', [Validators.email, Validators.required]],
        phoneNumber: ['1234567890', [Validators.required]],
        emailOrganization: ['1234567890', [Validators.required]],
        website: ['ACB', [Validators.required]],
        phoneOrganization: ['0123456789'],
        fullName: ['Nguyen Van A', [Validators.required]],
        ngaySinh: ['1/1/2001', [Validators.required]],
      });
    }
  }
}
