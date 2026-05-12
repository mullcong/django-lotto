from django import forms

class ManualLottoForm(forms.Form):
    round_number = forms.IntegerField(label="회차", min_value=1)

    number1 = forms.IntegerField(label="번호 1", min_value=1, max_value=45)
    number2 = forms.IntegerField(label="번호 2", min_value=1, max_value=45)
    number3 = forms.IntegerField(label="번호 3", min_value=1, max_value=45)
    number4 = forms.IntegerField(label="번호 4", min_value=1, max_value=45)
    number5 = forms.IntegerField(label="번호 5", min_value=1, max_value=45)
    number6 = forms.IntegerField(label="번호 6", min_value=1, max_value=45)

    def clean(self):
        cleaned_data = super().clean()
        numbers = [
            cleaned_data.get("number1"),
            cleaned_data.get("number2"),
            cleaned_data.get("number3"),
            cleaned_data.get("number4"),
            cleaned_data.get("number5"),
            cleaned_data.get("number6"),
        ]

        if None not in numbers and len(numbers) != len(set(numbers)):
            raise forms.ValidationError("로또 번호는 중복될 수 없습니다.")

        return cleaned_data


class AutoLottoForm(forms.Form):
    round_number = forms.IntegerField(label="회차", min_value=1)


class DrawLottoForm(forms.Form):
    round_number = forms.IntegerField(label="회차", min_value=1)