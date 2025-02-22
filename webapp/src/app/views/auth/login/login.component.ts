import { login } from '@/app/store/authentication/authentication.actions'
import { Component, OnInit, inject } from '@angular/core'
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, UntypedFormBuilder, UntypedFormGroup, Validators,} from '@angular/forms'
import { RouterLink } from '@angular/router'
import { Store } from '@ngrx/store'
import { ApiservicesService } from '../apiservices.service'

@Component({
    selector: 'app-login',
    imports: [RouterLink, FormsModule, ReactiveFormsModule],
    templateUrl: './login.component.html',
    styles: ``
})
export class LoginComponent implements OnInit {
  
  constructor(private http: ApiservicesService) { }

  form: FormGroup = new UntypedFormGroup({
    email: new FormControl(null, [Validators.required]),
    password: new FormControl(null, [Validators.required]),
  });


  ngOnInit(): void {
  }


  login() {
    let body= this.form.value
    this.http.loginOnSysteme(body).subscribe((res:any) => {
      console.log(res)
    }),
    (err:any) => {
      console.log(err)
    },
    () => {
      console.log('complete')
    }
  }
  
}
