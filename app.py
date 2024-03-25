from flask import Flask, jsonify, request, render_template, redirect, url_for
import random

app = Flask(__name__)

total_cards = 20
cards = [{"id": str(i), "name": "Try again", "win": False} for i in range(total_cards)]
uber_voucher_index = random.randint(0, total_cards - 1)
cards[uber_voucher_index]["win"] = True


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = next(
            (u for u in users if u["Email"] == email and u["Password"] == password),
            None,
        )
        if user:
            if user["Credits"] > 1:
                user["Credits"] -= 2
                random.shuffle(cards)
                return render_template("index.html", user=user, cards=cards)
            else:
                return "Insufficient credits. Please add more credits to play."
        else:
            return "User not found"
    else:
        return render_template("index.html", user=users[0], cards=cards)


@app.route("/pol")
def pol():
    return render_template("pol.html", policies=insurance_policies)


@app.route("/profile")
def profile():
    return render_template("profile.html", users=users[0])


insurance_policies = [
    {
        "policy_id": 1,
        "policy_name": "Car Insurance",
        "coverage": ["Accident", "Theft", "Liability"],
        "premium": 500,
        "deductible": 100,
        "details": "Car insurance is a financial product that provides protection against losses incurred due to accidents, theft, or damage to vehicles. When purchasing car insurance, individuals select a policy and pay a premium to an insurance company in exchange for coverage. Policies offer various levels of coverage, including liability, collision, comprehensive, and uninsured/underinsured motorist coverage. In the event of a covered incident, policyholders file a claim, and the insurer assesses and approves it, providing financial compensation up to the policy limits. Policyholders may have to pay a deductible before receiving compensation. Car insurance policies typically last for a set period, and at renewal, policyholders can adjust coverage or switch insurers. Understanding policy terms and conditions is crucial to ensure adequate coverage when needed, as car insurance is often mandatory for driving legally on public roads, with specific requirements varying by location and circumstances.",
        "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMREhUSExMWFhUWGBYZFxcYFxUbFxkgFRcXGRoZFhgYHiggGRsnHxoYIjEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGxAQGy0mICYwLTYtMC8wLzItLy0tLS0tLS0tLS0tLy0tLy0tLS0tLy8tLS0tLS8tLS0vLy8tLy0tLf/AABEIAOEA4QMBEQACEQEDEQH/xAAcAAEAAQUBAQAAAAAAAAAAAAAABAECAwUGBwj/xABHEAACAQIEAwUFBAUJBwUAAAABAhEAAwQSITEFQVEGEyJhcTJCUoGRFKGx8AcjgpLBFlNUYnLR0+HxFTNDg6KywiQlY5PS/8QAGgEBAAMBAQEAAAAAAAAAAAAAAAECBAMFBv/EADgRAAIBAgQCCAYCAQQCAwAAAAABAgMRBBIhMUFRE2FxgZGh0fAFFCJSscEy4SMVM0LxYqJDRFP/2gAMAwEAAhEDEQA/APb6AUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKA4ztb2jZLxsW7dy5kUM6IWVn7wEAqygnIu5IHtFRyM+hhcMpQzyaV9r8Lft/i55+KxLjLJFN24Ljf9L82Nr2Y402JsOYLXLLNbJ0AcqJBB2BOkxsZ5RXDEUVTmuT17Dvh6zqQfNadpr+Edor7Oq3jbDFHZrBtXbN1SqyFtG4Sl7YzqvWu1XDwUW433Wt01321XmcqeIm5JStttZp919GU/lyozA2QWCo4Fu8lzRri28rMBCuCw8Oo86fIvRp+Ka4X8CPnldprwafG3jr/YxPaW6b9uyUNp0vqt1AyOHV7Nx1hoEHw+UdaRw0cjle6a04WaaRLxMnNQtZp69jTaKXO3SqGzWgSEDgW7yXDrcS2VcqIVxnBiT60WAbtZ+Ka4X06tCHjlG914O/FLx1M2J7XPb77PhGH2cobsXUMLc1Urp4m6rsI3qscGpZbT/le2nFe/6JljJRzXh/G19eD29+Z1QNYjcKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoDQdoezQxV23dFzu2trcWQski4pA1kREn6mtVDEulFxte9vIy18N0slK9rX8yZwPgy4bDLhpzKAwYxGbOSTIB843rnWrOpUdTY6UaKp01TIX8krTAJcuXriKrKiO4KoHUocsKCSFJAzExXT5uad4pJ8Wlvx92OfykWrSba4X4e+stbsfZYgvdvOVRLYJZNFS4lxRAQDQoPvqfnJrZJa372rc+sj5OLs22+HDg78jNjuy1i9de65eXKlgGAXw23tgbSBlc896rDFThFRVtPW/6LTwsJycnfX0a/ZHfsZZZVV7t5gtsW1lk0VWRwAAgGhQa7nnNXWNmndJb379Vz6yjwUGkm3ord2j5dRNxnZ21d+05i//AKkWxcgjTuhC5NNPOZrlDEzjlt/xvbvOksNCWa//ACtfuNsBXA0FaAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoDBirBcCHZInaNZBGs7jU/ODyq0ZJbq5WUW9nYwnBv/AD7/AEX5jarZ19pXI+ZeMK2R1NwtmUgEgaSCJ09f9KjMrppE5XZq5XE4ZmbMtxk0iBEbzOtIySVmhKLbumWW8G4M98530IXnz25cv9IOa5EKD5lBgmhR3z6TrpqDGh+m++p9anOuSGR8y6zhXUgm6zAe6QsHSBynzqHJNbEqLT3JdULigFAKAUAoBQCgFAKArQCgEUAigEUBSRQFaAUAoClAKAUAoBQCgFAKAUAoBQCgFAKAUBUUAoBQCgFAKAUBzXaDtthsKSgPe3BpkQiAf6zbD01PlWmlhZ1NdkZquKhDTdnn/Fu3+LuzlYWl5BBr82Ov4Vvhg6cd9TDLGTltoaLEcUut7d129WY12VNLZHJ1W92bvsdwd8W/ePPcodd/GR7g8up+XOs9epkVluaKEM+r2PXeF21W2AoA1Og0/OkV5TiovQ9NNtakqoJFAKApQCgFAKAUAoBQCgFAKAUAoBQCgKigFAVoBQCgLbtwKCzEAAEknYAbk1KV3ZENpK7PK+2Pbp7xNnDEpb2LjR39PhX7z5V62HwSj9U9zyMRjnL6YbHFNbP4T+fzvW6x57mWNbO8fnrU2GYk8H4RcxNzIugGrsdlH8SeQrlVqKnG52owdSVkekcMW7YRbaugRYAAtAASf7Ukknc9a8qSzNt7nrxeVWRKuY++yjLc7oyZKqDPLUPP3RRQhfVXIc5W0djacAfEuSz3gyDSDbUE+jKRHLlWetFJrKaKUm07m/rmdClAUNAKAUAoBQCgFAKAUAoBQCgFAKArQFaAUAoCjMAJJgDcnagbseV9tO0pxjGxaJFhTqR/xCOf9noOe/SvawuF6NZpb/g8HGYzpXlht+TRWeGiNflPXlWpyMViX9gB5R/mZP4VXMSUHBzccIm51np1J8qOqoxuyYU3Ulliddw7Aph7fdoPNjzY9T/dyrzKk3UldntUqcaccqMlw7dA0n0gj+NVRdlHMn15czO1SQdfgMN3dtU6DX1OprHKWZ3NcY2ViRVSxQ0ANAUoBQCgFAKAUAoBQCgFAKAUAoCooCtAKAtdwoJJAA1JOwjrRK+hDdldnmvbPtWb82LJIt+83N/7l/GvYwmEyfXPf8Hh43G5/oht+f6OcwdnnHzOw9OtbZM85GytwP765snMZkOcqijVjAJ05Ek+kAn5VSUlBXkdKcZVXlgjocJhltLA1J9puZ/y8qwVJubuz2aNGNKNl3sPcqLHS5Zm50IJnZ7D95dzH2bevqdln01+lUqvLG3MvSV5X5HW1kNRoO1uJvoMOMOQHa9GUxDhbdxyhJ2zZYmtOGjTlmz7W8NUrmbEymsuTe/jo3bvNRhu0GJRrvehQz3bCor6JYF5GYC4QJJAAB6sY0rvLD02ll4J35uz4e9jhGvUTebmrcldcfe5mw/aG9cvYcTbVGOJVwNVuGw6LNpjqZnwjqTMwKrLDwjCW9/pt1XT3/ZaOInKcdrfVfrs+H6MQ7Y3O6a5kstNg30COxKQ6Lkvefi3EaqwjSrfJxzZbve2q360V+cllctNr6PyZuuM3cQmF70QLtvLcdU1VlQy6AsJMpOsDUCs9JU3UyvZ6a+T8TRVdRU8y3WvqvA1X8oboTv11XEXyljMDkRERoaBDEuUYgT7w6V2+XjfK94q762/S5x+YlbMtpPTs/uxgu9osQr98FXJ3GGd7bMSB3l64hNsqIJOhk8gNKusNTay31vKz7EnqVeIqJ5raWV12u2hnTj9xSbam2C17GeO+5CAWHAyggbmfkAd6p8vF6u+0dlrqi3zElorby3fJ++wpd4/dtPdUQxbElELSUQLh7dyBl1MkmPUnlFFh4ySf/jd9f1NEuvKLa67eSZ03DMUbtm3cZcpdVYrIMSNgRuPOslSKjJxTvY1U5ZoqT4kmqFxQCgFAKACgLqAUBgxuKSzba45hUBJPp/GrRi5NRW5Wc1CLlLZHmfHe0OKxhyoipZEQpc5m13cqunLTWK9ihho0tXqzwsTjHWeVaI1Jw1xdbthgo2NrxoPUCH+cGtGZcGY3AmWEVxnVgwHwnbyPwnyMVF7aFXG25nwlhrh5Ko3Y/gOpqlSooLrL0KE6z5Ln6E3B3FE3F2Iy253yyCXPm5AP9lU21rA7zeZntQhGlHJEkLjJqcpOYzOZEjX0ioJMBJ56DoP4n+FSQdd2cw2SyCd38R/h9341krSvI1Uo2ibSuR1IuNxFtGtB93fLb0nxZWOnTQNrV4Rk07cFr2FJSimr9xYbuHcOc1pgQDc1QiI0L+UbTU2qJrfq/oi8HfbrGbDwpm1CAMh8EKDoGX4RykUtO731F4W4aFjHDKHnuQCf1nsCTMePqZ60/yO2/Vv5D/Gr7dZnuYu2IBuIM0RLLrm0ESdZqqhLgiznHiyxhZP6g92YA/VHJoBt4OnyqVnX169v9kfR/DTsK2Us3FlRbdYCyMrCFOi6cgeXKjzxdndBKElpZl9zB22GVraETmgqpEn3oI386hTktUyXCL0sLmEtsCGRCGMsCoIJ01II1Og18qKUlqmHCL3RlURoNqqWK0AoBQCgFAVFAVoDFiMQlsZnYKJAkmBLEAa+ZIHzoDiP0hcTLumFQ6Dx3foci/x/dr1MBRsnUfd+zxvidfVUl3/AK99hpMPbyqv7P8ACtz1Z5d7G1s34ri4l1UsQuM2VI7xbRa9Kqht+FyWMAMwIlesnaudSo6cDth4dNUS4cewh44YpybS4VlEAspu2pCkkBZzGM0EdYDVkU1azu3xftnr9G1tZcl7RDGKxZum0cJcJVQ5ym2RDEqPe6g/Q116WC01KdFLe6F7jAtf75LlrzuIyr+8RH31KnB7Mq4TXA2XD+NIYhgVPQzUunfUhTtub+3bF2MuoJAmetcW8u53SzbHaIoAAGwED5VhNhdQGv4rgDdawwIHdXRcMzqMjrA8/EPpXWnUUVJc1bzTOVSDk4vk7+TOdsdjSltU/VSMOttozrmZby3M+ZYPLQ9eRGla5Yy8r6737rWsZVg7Rtptbvve+gxPZbEsmXvrRL2VtXCVPuXmuKVywDo2UkgbTGtRHFU075Xo7rwt+v0JYWo1bMtVZ+Lf7/ZKfs2wW7kNvPdxLXXJHtoSSLZaCVgkGR0PU1T5lNq97KNl1PmX+Wava13K761yITdi2NoozWy32fulJU+E989wMJGgggadK6fOpSur738rHP5JuNnba3ncnXOzbn7Qma1kv98e8yE31N4RlmYyjbfVQB51zWJSyvW6tpw09+Op1eGbzLTW+vHX34aE3s7wlsOHL5czlZyE5fAoUGCBB9BsBvE1yr1VO1tkdKNJwvfibiuB3FAKAUAoBQCgFAVoCtAa/j2Pt4fD3Lt0AqFIymPFm0Cwd5Jj510pU3Umoo51qqpwc3wPLMBaLeM7sZ9OgHkBp8hX0FlFKK4Hyrk5yc3uzaZNB8qpxIlsZSOfOoRzky9MYiXPFqbaqwXbNcvylpQToGC556C8Cdq83ETzTtyPf+H0clK73l+DbB+5GSBcvXCWIGgY6Au3wW10WTyCjUnXhsbTJYs5AZOZmMu0RmMRtyAAAA5Ac9SbJENlxuaEVaxW5pOIdmMNd8fdi22+e2cjftZdG/aBqU8uxDV9zJ2V4JicPiVi4L2H96QFuLPsn4W110j0qtaq3GzJo0kpXR6FWU1CgMGJsM8Zbj24+EWzPrnVvuq0ZJbq/j+mVlFvZ28P2YPsNz+k3vph/wDCq2eP2rz9SuSX3Py9Cn2G5/Sb30w/+FTPH7V5+oyS+5+XoPsL/wBJvfTD/wCFTPH7V5+oyS+5+XoPsL/0m99MP/hUzx+1efqMkvufl6D7C/8ASb30w/8AhUzx+1efqMkvufl6D7C/9JvfTD/4VM8ftXn6jJL7n5ehlw2HZSSbrv5MLQA8xkRTVZST2SXj+2WjFrdt+HoSKqWFAKAUAoBQCgKigK0B5d27419pxAwymbVokPGzOdD+6JHrNe1gaGSGd7v8f2eD8SxGefRrZfn+jBw1YXKd1ifPTQ/OPuNaJ8zz1yNgqfn5VQhjEYi3aAe4cqTqeWiljJ5CFOvlXKrUyRudcNQ6aolw4mpwOONwo+UZ7pLAMDCZmtmX28WQKgXfKg1GY15qVz6J6HSYK4qTBlm9pm9puk8gBrAGg5CumQ55zYB5qLWLXLGoC0EkgDcmAOtSQdPgcMLahee5PU1llLM7mmMbIkVUsKAiYvEMHS2kZnDNLSQoTKCYEZjLKIkbkzpBvGKs5PYpKTuooxXOI93o6klVzXGSMiAlgGOYg7KSQMxEehNlTzbd3X77irqZd+8xNxtZMWrpjvdQE1Fl8lwiW2BjeCZETU9C+a4eauuBHTLk+Pk7MyjialsuV8oYJnhcmZgpUb5tcyiYiTFV6N2vfuLdIr2t3kYdobUIxDKHVXGbICFb2WKlpg66AE+E6bTf5eV2uXbv4FOnjZP3Yut8aADG4rLBuw3hysLV3u4HikHVd4BnTSodF6ZXy81clVlxXPydgOOoR4UdiA5YL3Zyi3kLSQ+U6XFMAnfqIqeglxfLnxv1dRHTx4Lny4W6+sytxVczKAZUpJOUjxsoHhzZo8W5AGh3516J2TfX5d1i3Sq7S9/spe4zbUSZ5yPCIIfu8pJIAJbNGseBtdKKjJu3va4daK99diVgcWt5A67EkctCpKkaEg6g6gkVScHB2ZeE1NXRnqpYUAoBQCgK0BzXb3tF9iw5yn9dclbfUdX/AGfxIrVhKHSz12W5lxdfooabvY8p4EvtdTE/fv57178tj5qTuzqLAmCNx9/ka4Mi5sLJkVzehN7nEduQ2JdUt5B3Cu5dmOXdBlPugzrsYCk+VebiJOcrLge7gKXRU7vd+0XcJ7RlmtWL693ctMQToFgq0agxM5ddjIM1WE9UmaZwdnJHUNeIOoJ8wNfmBv8AKtVjLczWOIFdjIqrhcsp2NrYxgcb61zcbHVSubzgOC/4rbnRf4n5/nes9WX/ABR2pR4s3VcTsKAUBF4ilvLnunKqeLPmK5eU5gQRV4OV7R4lJ5bXlwI2JwuHQgPI8JJl7kFUJY96Z8Sgk+38RHOKtGU3t+t3y/opKMFv+/P+yRawlsiQpgi5vmBi8wd5B1EkT5eVVc5fjy2LqEfz57mEcOtoWuGd8+rNlGVAoJWYJAXcifoKnpJNKJXo4puRdcwlpFD6qttBqHdfCgkBsp8QEc53PUyU5N25/klxilfl+Ct3B2hCsPaLhdW3uE3GgzoZUmeUaRRTluury0DjHZ+76l4wKc8x8LrLO7GLmXMJJ/qr6RpUdI/fUTkXvrLTw62TmIJMQJdyBqrQoJgaop06U6SVre/eo6ON7lW4fbOc5dbhVmILAysZSCD4YidI1JPM06SWnUOjjr1mWzYC7FjpHid22JPvE66nX0HIVVybJUUjLUFhQCgKUBUUBdQHhHbTi5xeOdplEPd2xyhSQT8zJ+lfQYSlkprmfP42rnmyvDVyn8/hWmR5rN/YeK4tEXsZr10nwIGLOCDl90bG4xkQFkcxJjUakZcTUyRtxNmBo9LUu9lv+kcZh711Eu2HUqTbLK9weO5aIYW2jqfESZ9pzprWOGsWe3PSSJnEOF2L4l2uC6dru7ehBhSu/hgDXSDrXWeHUkco13FmDA8YuYUrYxJlDpbvCcumytOogddR5jWuabpvLPbmdGlU+qHgb13nUEa8xsfXr+da1IzM2HZvCvib4TUBfE7An2RyB6k6R69K51pKEbl6MXOVj1FVgQNhXlnplaAUAoCFxHDPcKAFQoOZswzSV9lSsiRJzTO6L1rpCSjfmc5xcrcjW3uCs1sqwRmFi7aVjuZ0QkkEjTfzmuqrJSur7p+pylRbjZ8mvQztw1hclVUDOhVwYKIoXNbCxsYbQGPGTuNa9IsuvX3vn75FujebT2uREbgjiytvKrt3OQlnYZbhWDcDQSSds2hAUAaExfplnb215cOXvcp0MlBR3058eZXHcJvObkZQWS4kyACGtMqAwuYw2WZMCJA6IVYRtfq/PbYmdKTvbr/BmHDLmbMoW0JBChi0Hu7ym4NBJJdPM5JOulV6SNrPX/taeT8Sejle60/6evmZuEYN7UyN8oIzggZQ0uAEEkkqCTqYBMRrWrNS9+W5anBx9/0bSuJ2FAKAUAoBQFKAuFAR+I3+7tXH+FGb91SatBXkkVm7RbPnbhyTvvoT19T5V9Oj5iozf4Zvz/pRmZk63iDOWZPKOflrzqtla7OTbbstzcFAEFhdTcE3j/UXdf7JJyAf13NeRWfSTu/aPpMLSVCkorv7TX9rOANjlEOEa1mKGNyw1Rm5IRExzjpVWtNDsnZ6nIYbiEgqwKupIdD7Skbgj8yINaYVLozyp2Zfcx1tlKOMyncEgD/I0lJNWZEYtO6ItnGNh/CDmtHadSn+X5334fVR21j+DR9NbfSX5PbP0eYVFwi3FdXa74nZTIB5J+ztHWay1qvSSvwNFGnkj1nT1xOwoBQCgNZxe+6sgXvIIuEi2LZY5Qse367DXUV1ppNO9uG9/wBHKo2mrX7rfsjYXiz+BYD+G0S06sLrEAyoy6ASY0JkCNKvKktXtv5efoUjVei328y4cXfwLlRXdwsMTChrdxwQRpc9ggQdfKKjolq+CX7S7tx0r0XFv9N9+xT/AG2xVmCr4FzMMxlv1jp+q01nISCd8yjSZqehV7X39E9fHXkOmdr229WtPDTmXDilzU92pE3wgDak2bhQTIA8UddNN50joo8+Xmr+RKqy5c/J28zFf4qxAKkAzaBklVk32tsCGEg6R9w61MaS49f4uRKq7XXV+bC/xdlYEgGBcUhTKki7YQNMTA7wyOUMNYmpjSTXh+G/0HVafj+Uv2bPA4kuPEAGBIjrBiQDqPQ7GRrvXGcbPQ6wldakmqFxQCgFAKApQFwoCFx1Jw18DnauD/oNdKX+5HtRzrf7cuxnz9w5QNCx+hj1YyZr6ax8zOVzaKwA9r5QRUmWRu+B2wAbzwAAcs8gB4n+k/fWLF1f+C7z0Ph+H/8Akl3epu+FWSQ1x5DXIMHdVHsIekAkkfE7V53Wex1E17PQ9fvqbkWOB7f8EVIxCMEuDwga/rR8JjUuOTfXqK1JqKzcfydKNKVSWRbc3su85a3w3E3fZsPHOVbX1FY54yq/4Q8T1qXw3CxX+Wtr1e2bThfA79plcggoQwBWRI20OhrO6+KeljXHDfC48b9rZscJxTE4G616xMNrctKhyHzCKCFPmB9RpSnOptNd5yxNHDWzUZrsb37DorP6RLrDNmgc5A8J+FvhP3HkTSUqkXaxajSwtSN72fJuz/snYb9IFyJJQr1jT61Tp5rdHb/T6Mv4y80dFwbtS14+K2APEREyQuXMQOcZln1rrSqOettDDi8NCg8ubU6W1dDqGUgqRII2PpXYxF0c6AsOHSQcqyswYEid46TU3ZGVGJ8BaMA21gMWiBBJUqSRsdCd6spyXEhwi+Blawpyyq+H2dB4f7PSq3ZNkGtKRBAjXkOe/wBaXYsi0WEjLlWIiIEQOUdKXd7jKtiq2VAgKAAIAgRB5R08qXe4shbtKoAVQABAgAQOgjlRtvcJJbF9QSKAUAoBQFKAuFAa3tHixasMT7xVP3jB+6a74eGeokcMTPLTbPBcRh2t3WQlYzGDMEa6GIr6NO6ufNyS2Nlw2x3twI5A3J6wsTH1H1rnVqKnG/HgRRodLO3Dj76zdY7F52FoexbjN0kQUt+nvHyCj3q81Ru/ye1fKvwSLOOPWrOBRSJGK4wtlGuOdBEAbsTsq9Sa41LQV2aKUXOVl/0c3ad2VuIYj/fAsET3bSqxBUDrC5p6rWBtt3Zu0StHY2V/F9xaEHxRr5k8z6UIOaxHFb19myQuRRLakCCq6AESdfzrEkGz7K8YfDXxluGGDZhcdgjEKYLZQcvlA3ijJNp2pxttv/WWWtWsWkeO1eY95JAyurWgG9T05wKiwLbnbQY3CHDsvd3pGZeTgGSyeWkkfiNarN2i31M6UY5qsV1r8nQ4RwmGs3V2tFbnqt2Rc+UNP7ArlQVqaNHxBt4md+Dt4aG9w2PTCXSjmLV3xL0Vj7XybQ+sn3qvKai1c5UqE6qbjurHRWbyuAysGB2IMirJ32OMouLs0X1JAoBQFDQFKAUAoBQCgFAKAUBQUBcKA4T9KmPyLYtzuzOf2RH/AJGvT+Gwu5SPN+Iy0jE814hN4qV1c5RA3JOn91esmo7nkOLk7E3H23wt/DIiZrjJfUv7kuLRJY8wuQabkTXl1ajnNNdduo9SjSVODj2X6yZogygk9Sd2J1LHzJ1rpGNkVlK7I3ExfNsdwVQz4mYgQAOU6annWXGSqRheD7Tf8NjQlWtWTa4Jc+41uBx9zPbbFJcuC3JXIFaSZ8T+ISQCBtyPWvKWJzJZ3t7ue1XwLjJqjHR6v9JdS832IzLx6zcVkfOsvdMG2/vuxEwDyI+tW6emuJx/0/E/YyHjMU1xVAzmVGYhHJGgkDSMxPPb6VPTU+ZT5LEfYzFaxaIsFLyyNf1VyOWggHQf586npqfND5PEfY/Ao2Nw595x62bwH/ZTpqf3LxK/KV/sl4MjPxHDjY3G9LNyPvAqemp80PlK/wBkvBk1uI2sRhkspbui4jXHFwpkKkxARpk6CY8h5VxrYiMY3i02bcB8NnWrZaqcY8Xt1LfrOibtFfwtpcNiRbYXUItXxGS4mUBlI0CuMwE6CdPOpnKWROmlfkcqVKk8RKNeTtdpvrvu99PE3N/vL62+9R1VQoiAGK84knkBr6dKySc5/wA1Y9alClQvGjJPr37NdDqf0f4sNbuW59hhp0kf5D61ow0rpo874pTcZxlzR1laTyxQCgKGgKUAoBQCgFAKAUAoCgoC4UB5L+lzETirafDaH/Uzf3Cva+HK1NvrPIx7vUS6jlOzOLyYywdNcy66iSGA0+YrviY5qbTOGH0qJm37U3Yaw3wXlB/5ga3+LCsaVrPr/o1XvddX9kTH8Xt2jl0Z/hmAP7R5em9Z8VjYUNN3y9TfgfhVXFfVtHnz7PdjXJiLl8yxGUEwo0XQb9TuNTXhV8VUrP63pyPrML8OpYVXgteb3M+ItkhVAgsYneAASSPPTpzrga4x4ltnhlpTqwggn6EAyT6j76iy4nXNLgSLbYZfZGc/1QW/7aj6UTlqMzDED3bB+YUfiaZh0b4sw38U8hRaEkwNRPrAFRe5bo4pXubAtZcKmIdGIMhVUekO6jxekx1Jq+eL0kzP0dSLcqaa98EYON23Fy3cS2hW2cqoDqc4iWgAKoOkTzpLe6O+FlFwlCUmr637OXWbbB8NBtCzcRSCPEseDU6wOWs6iusU1Y8+tOMnJrb3uR+4vcNUgZr2D263LE9PiT8B056v5LXc8vWk7w1XL09DpP0fIe9W6j5rd5L2YAgrmRrWVvJozCD8IqKFNwWu5X4hiY139LuklbzPQ60nmCgFAUNAUoBQCgFAKAUAoBQFBQF1AeKfpYf/ANwI/wDit/8AlXufD/8AZ72eRjV/k7jluEAnF4cD+dT/ALhP3VorfwZnor60dB2rSQ6TlnUN0IMg/IwflXn1JJUXLkjdRg514x5v/vyIXFOG4e5dcWiVcQACDlcjSWkDLPhOcEg55MakeHWw6nrxPpMH8SlR+mSvHzXZ6Gut4ciUYQQYIgggjcGOdeW7xdj6mLjOKlHVMk5HIBBEKZkgnkRpB10M/KpTZbLFGZ8ACRn8Wh13HLlP8KXClyJVnQQCPkNPpOnpUXDjxMpvlfhPlEGozEZEydhOz19/GQtsMPbuNl3+FdWj5a61ohhqsuFu0wVfimGpaXzPq9diXwXs5YzhjeLkmFyrAMiZUt0EnbTcxXWOCUXdswVvjkpK0IW7X6WMPH8IFg2S7O7hLaMRkafjhZAIG461RUlKdka44ucKDnOK0Xfd6LjzZN7OYpr1lDcUJcU3LdxBsrW3KsF6LOoHnXdqzsYac88M/P8AOz/BP4rf8JQaltI+VVqPSx1oQ+pSZoeFcMxGGtd/g2LAgm9bQkFSpyMVHy5DToRoKTp1Uo1E9UvfajJWqUJ1p07WV3b37R6P2X7S2sYgymLgAzI0Zh56aEHqNK0UMSqmj0fvYw1sPKm+o3taTOKAoaApQCgFAKAUAoBQCgAoCooDxT9Mlspjlf47Kf8ASzg/w+te18Ol/ia6zzMbH60+o5js204hX5IGb7so+9vurTX/AI2M1PR3N/2vvJcwpb3gyAejNr+BrxsfeNCSPc+CQVTGw7/wQsN2buIqPnABVWPt5l0mIWZjbSvA/wAy/jI+zqRwdS8Z01pfXbz0JTcNS4rv9qttcPxGP35M7Vqhgb61JXZ41X41k+jDwSitr+hw3Eu0t6y7W17p8pIzIHK6dCd66fKUlw8zN/q+LfFeCItrthiR7ikDllb++q/KUuT8S/8ArGK5rwJ+G7cmR32HzD+qSD8pFUlgocGaKfxyqv5RXcb3hvbAo5vWLVsAwPGCzrvsdMpPpyrgovDzvY9aHQfE6GXpGmt1t4rW67zNc4xxC8SczwZ0CIF15SRJHqTVpYuo9kisPgeBh/Obff6I32F4xfW2xdBmykZUyqGG/jgEkk8ttq5vEza1IXwrCxqLI3br4dm3mZ+yuPfE4pe9UIELZUg6QhGpOpMsv0rthHmk2ZvjlKFClCMHe7u32EwObd/Eg6DvS379u2fxmrVX9bM+EhehHrv+WRMfxWzhl77EXMgb2BE3H/sJyH9Y6Up0nPV7EYnFwo/RHV+S7fQ6j9FWJFzDhzEmTykFnY5fPrPMk1ttbQ8OUnJuT4krtJ2Rzt9pwh7u+JMCAGneOQJ89Dz61ir4XN9UN/fgzXQxNllnqjL2Y7VG632fEr3d8SNQQGjeJ2PkfvGtVoYp3yVN/e4r4ZJZ4ao6ut5jKGgKUAoBQCgFAKAUAoAKAqKA8s/Ttgv1eGxA912tn9sZhP7h+tej8OnaUomTFwukzz3gIK2mfm5gei/5k/St1WRhSJ+Jwdy7hwYIQ3FTOfZzOGy6+TdNprzMa45FGXFo9T4YqiqSnTumotp9ln6mTg/aW4xa1icsgm33i6ayVh1Om490/IV5cqLTzR4cD2qOOVRdFV46XXWReL22QwcO18RrlVX+RB1n5V3jiKctmYquAxFJ/VF9q1RqGxmBX/e4F09bRX8DV7pmZprcs+3cKP8Aw2X/AO0fg1ToRcuTE8NJ8K6+fen8dKaC50nBMGM4cW1VAN8oE6aQY16/Ks+JlDJle56XwynVdZTjolu+rl1mbE9oMODAuBz0TxH7qxRw9SXDxPZqfEcPT0bu+rX+hw7GHEWzdAyIveTm1aLYmcojc6ATXRYPS8mZpfGbtRpw35v9L1Njwu4oxlslSZW4SR7pAQZjHKAV15uKnB6pvsOfxtu8I8r/AJM3F8dluMQue6wQhWACqSi+K6BudoUV36FObkzCsZKFBU4aPW779kc9iexOI4gwa/f1knNk1ExoDO2g08q7GE9I7J8EGAsC2bpYA6s0LqeQ5VDaSuyUm9EdbYuedSQcj+k60Fspi00vW7tsAjdgzRB9N/TMOdYsZRjKGfijbgqjz5Hszs+GYrvLVtz7yg/UV3w889KMnxRmqxyzcSVXY5lKAUAoBQCgFAKAUBSaAse7FAcn+kfD/auH4i0BLhc6DmWtnOAPMwR8660KnRzUis45lY47gXZ62tq219hkCrlSYzaTLnkDvA11+Vaa2K4Q8TJTw13mn4E7tDxTD3LPcllyjKVC7KUIIiIgaRpyJrBOKmrSPRo1Z0ZKdN2aPJ7+Iw6XXZWu2LjE5oJgyZnUZWE671Xo5L+MvE0fM0Zf7lLXnF28ndGMWcztctYpRmYnKZ3O+zaa61TotLOKZo+cWZunVnFcmn+n+iZbxWNT2b6t6XGH3GajoY/Z4P8Ast85Vf8A9hPtj6xM3+1Mf1B/bT+K06OP2y994+aq/wD6U/BehcOKcQ5SP+Yn/wCajoofbLzJWKr8J0v/AF9DKmKxjo4uGc2UBe9USJlvEokbAbbE1XooqScYP33l3ipzpyU6sL6Wt57IxfY2gju7Sz8V67cA/ZIitGaXCP4PO6Kn/wAqi7k3+kbLAYm3Zs27L3CVt/CLaBmLFszs5M6nQRpArlOFWas7JGmjWwmHeaKc5c3ol3X/AC+4ncC4gl7GKEbwi2QSDIJLoQCQADBCtp8Iq1Gj0SaucsbjPmZJ2tY6+zw8XLrXG1kjXrlAUH6CupiOgw1tVECgIvabg4xdjID40YPbPRlmPSQSJ865VqfSQcTtQq9HPMQuCdrgq91iFZbieFoUnUdVGq/mCax08TKkslRbGqphVN5qb3MfEbjcUvJaUEWLZzGQQSdpIOo0JEmNzEk6c6s54mWSO3vcvTjHDRcpfyO8sKFUKNgAB8q9OMVFKK4Hmttu7JCtViC4UBWgFAKAUAoBQCgLGFAYLqUBr8RYmgOdxvZyy3/CAjQRpEcgOVAaXFdlbfJYoDRY/sWje7PrQGlxPY4rsn0oDXXezbD3PuoCM3AmHu0BZ/sZvhoC9ODt8P3UBJtcIue6v5+lAS/5NYq6pTKpU9f9KA6Hsd2DxNi6Ljsqr0GYt8tqA9Ls4CBEUBJXB+VAVbhqncfef4UBFxPZbDXYNy1njYszkj0M6VDinuiVJrZkvAcDs2RltoEHQFo/HeiSWwbb3NnbtxUkGVRQF4oCtAKAUAoBQCgFAKARQFjWgaAxNhAaAwtw8UBjPC16UBaeEr0oC08Gtn3R9KAtPAbXwL9BQFP5P2f5tfoKAqOA2f5tfoKAypwi2NkX6CgM64JRyoC8YYUBcLFAXC1QFe7oCuSgK5KArloCsUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKAUAoBQCgFAKA//Z",
    },
    {
        "policy_id": 2,
        "policy_name": "Home Insurance",
        "coverage": ["Fire", "Flood", "Theft"],
        "premium": 800,
        "deductible": 200,
        "details": "Home insurance is a financial product that safeguards homeowners against financial losses resulting from damages to their properties, including the physical structure and personal belongings, as well as liability for accidents that occur on the property. Homeowners purchase policies and pay premiums to insurance companies, selecting coverage options such as dwelling coverage, personal property coverage, liability protection, and additional living expenses coverage. When an insured event, such as fire, theft, or natural disaster, occurs, homeowners file a claim with their insurance company, which assesses the claim and provides financial compensation up to the policy limits. Like car insurance, homeowners may need to pay a deductible before receiving compensation. Home insurance policies typically renew annually, allowing homeowners to adjust coverage as needed. Understanding policy terms and conditions is essential for ensuring adequate coverage, as home insurance is often required by mortgage lenders and varies in requirements and options based on location and individual circumstances.",
        "image": "data:image/jpeg;base64,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",
    },
    {
        "policy_id": 3,
        "policy_name": "Health Insurance",
        "coverage": ["Hospitalization", "Prescription Drugs", "Surgery"],
        "premium": 1000,
        "deductible": 300,
        "details": "Health insurance is a financial product designed to mitigate the cost of medical expenses for individuals and families. Policyholders pay premiums to health insurance companies in exchange for coverage that helps pay for healthcare services such as doctor visits, hospital stays, prescription medications, and preventive care. Health insurance policies typically offer various types of coverage, including hospitalization, outpatient care, emergency services, prescription drugs, and mental health services, among others. When policyholders need medical care, they may be required to pay a copayment, coinsurance, and/or meet a deductible before the insurance kicks in. Health insurance plans may also have networks of healthcare providers, and using in-network providers can result in lower out-of-pocket costs for policyholders. Understanding policy terms, coverage limits, and network restrictions is crucial for making informed healthcare decisions. Health insurance is often obtained through employers, government programs, or purchased independently, and regulations and coverage options vary by location and individual circumstances.",
        "image": "https://www.sanlam.co.za/personal/insurance/healthsolutions/PublishingImages/health-solutions-banner-desktop.png",
    },
]

users = [
    {
        "id": "1",
        "Name": "Alex",
        "Last_name": "Lazarus",
        "Date_of_birth": "4 Jul 2002",
        "Password": "Alex1234!",
        "Email": "alexdylanlazarus@gmail.com",
        "Phone_number": "0633603171",
        "Credits": 100,
        "Street_Address": "2 Tree Street",
        "Zip_code": "1999",
        "Suburb": "Beverley Hills",
        "City": "Cape Town",
        "Country": "South Africa",
        "sex": "Male",
        "policies": insurance_policies[1],
    }
]


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/after_login", methods=["POST"])
def after_login():
    email = request.form.get("email")
    password = request.form.get("password")
    go_ahead = next(
        (
            user
            for user in users
            if user["Password"] == password and user["Email"] == email
        ),
        None,
    )
    if go_ahead:
        return render_template("index.html", user=go_ahead)
    else:
        return "Invalid email or password"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Retrieve form data
        first_name = request.form.get("Name")
        last_name = request.form.get("Last_name")
        date_of_birth = request.form.get("Date_of_birth")
        email = request.form.get("email")
        password = request.form.get("Password")
        phone_number = request.form.get("Phone_number")
        street_address = request.form.get("Street_Adress")
        zip_code = request.form.get("Zip_code")
        suburb = request.form.get("Suburb")
        city = request.form.get("City")
        country = request.form.get("Country")
        gender = request.form.get("gender")
        new_user = {
            "Name": first_name,
            "Last_name": last_name,
            "Date_of_birth": date_of_birth,
            "Email": email,
            "Password": password,
            "Phone_number": phone_number,
            "Credits": 10,
            "Street_Address": street_address,
            "Zip_code": zip_code,
            "Suburb": suburb,
            "City": city,
            "Country": country,
            "sex": gender,
        }

        # Add the new user to the list of users
        users.append(new_user)

        # Redirect to login page after successful registration
        return redirect(url_for("login"))
    else:
        return render_template("register.html")


@app.route("/cards")
def get_cards():
    return jsonify(cards)


@app.route("/cards", methods=["POST"])
def post_card():
    new_card = request.json
    card_id = [int(card["id"]) for card in cards]
    max_id = max(card_id) if card_id else 0
    new_card["id"] = str(max_id + 1)
    cards.append(new_card)
    result = {"message": "Card Added Successfully"}
    return jsonify(result), 201


@app.route("/cards/<id>")
def get_card_by_id(id):
    filtered_card = next((card for card in cards if card["id"] == id), None)
    if filtered_card:
        return jsonify(filtered_card)
    else:
        return jsonify({"message": "Card not found"}), 404


@app.route("/cards/<id>", methods=["DELETE"])
def delete_card(id):
    id_for_deletion = next((card for card in cards if card["id"] == id), None)
    if id_for_deletion:
        cards.remove(id_for_deletion)
        return jsonify({"message": "deleted successfully", "data": id_for_deletion})
    else:
        return jsonify({"message": "Card not found"}), 404


@app.route("/cards/<id>", methods=["PUT"])
def update_card(id):
    update_card = request.json
    card_to_update = next((card for card in cards if card["id"] == id), None)
    if card_to_update:
        card_to_update.update(update_card)
        return jsonify({"message": "Card updated successfully", "data": card_to_update})
    else:
        return jsonify({"message": "Card not found"}), 404


@app.route("/users", methods=["POST"])
def post_user():
    new_user = request.json
    user_id = [int(user["id"]) for user in users]
    max_id = max(user_id) if user_id else 0
    new_user["id"] = str(max_id + 1)
    users.append(new_user)
    result = {"message": "User Added Successfully"}
    return jsonify(result), 201


@app.route("/users/<id>")
def get_user_by_id(id):
    filtered_user = next((user for user in users if user["id"] == id), None)
    if filtered_user:
        return jsonify(filtered_user)
    else:
        return jsonify({"message": "User not found"}), 404


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    user_to_delete = next((user for user in users if user["id"] == id), None)
    if user_to_delete:
        users.remove(user_to_delete)
        return jsonify({"message": "deleted successfully", "data": user_to_delete})
    else:
        return jsonify({"message": "User not found"}), 404


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    update_user = request.json
    user_to_update = next((user for user in users if user["id"] == id), None)
    if user_to_update:
        user_to_update.update(update_user)
        return jsonify({"message": "User updated successfully", "data": user_to_update})
    else:
        return jsonify({"message": "User not found"}), 404


@app.route("/policies", methods=["GET"])
def get_policies():
    return jsonify(insurance_policies)


@app.route("/policies/<int:policy_id>", methods=["GET"])
def get_policy(policy_id):
    policy = next(
        (policy for policy in insurance_policies if policy["policy_id"] == policy_id),
        None,
    )
    if policy:
        return jsonify(policy)
    else:
        return jsonify({"message": "Policy not found"}), 404


@app.get("/pol/<int:policy_id>")
def get_policy_page(policy_id):
    policy = next(
        (policy for policy in insurance_policies if policy["policy_id"] == policy_id),
        None,
    )
    if policy:
        return render_template("policy_details.html", policy=policy)
    else:
        return jsonify({"message": "Policy not found"}), 404


@app.route("/policies", methods=["POST"])
def add_policy():
    new_policy = request.json
    insurance_policies.append(new_policy)
    return jsonify({"message": "Policy added successfully"}), 201


@app.route("/policies/<int:policy_id>", methods=["PUT"])
def update_policy(policy_id):
    policy_to_update = next(
        (policy for policy in insurance_policies if policy["policy_id"] == policy_id),
        None,
    )
    if policy_to_update:
        policy_to_update.update(request.json)
        return jsonify({"message": "Policy updated successfully"}), 200
    else:
        return jsonify({"message": "Policy not found"}), 404


@app.route("/policies/<int:policy_id>", methods=["DELETE"])
def delete_policy(policy_id):
    global insurance_policies
    initial_length = len(insurance_policies)
    insurance_policies = [
        policy for policy in insurance_policies if policy["policy_id"] != policy_id
    ]
    if len(insurance_policies) < initial_length:
        return jsonify({"message": "Policy deleted successfully"}), 200
    else:
        return jsonify({"message": "Policy not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
