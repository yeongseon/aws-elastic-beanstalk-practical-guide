using Microsoft.AspNetCore.Mvc;

namespace GuideApi.Controllers;

[ApiController]
[Route("demo")]
public class DemoController : ControllerBase
{
    [HttpGet("env")]
    public IActionResult EnvironmentProperties()
    {
        var safeKeys = new[]
        {
            "ENV_NAME",
            "APP_VERSION",
            "LOG_LEVEL",
            "ASPNETCORE_ENVIRONMENT",
            "AWS_REGION"
        };

        var values = safeKeys.ToDictionary(key => key, key => Environment.GetEnvironmentVariable(key) ?? "not-set");

        return Ok(new
        {
            environment_properties = values,
            note = "Only non-sensitive properties are returned."
        });
    }
}
