using Microsoft.AspNetCore.Mvc;
using System.Runtime.InteropServices;

namespace GuideApi.Controllers;

[ApiController]
[Route("")]
public class HealthController : ControllerBase
{
    [HttpGet("health")]
    public IActionResult Health() => Ok(new
    {
        status = "healthy",
        timestamp = DateTimeOffset.UtcNow
    });

    [HttpGet("info")]
    public IActionResult Info()
    {
        var safeEnvironment = new Dictionary<string, string?>
        {
            ["ENV_NAME"] = Environment.GetEnvironmentVariable("ENV_NAME") ?? "local",
            ["ASPNETCORE_ENVIRONMENT"] = Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Production",
            ["AWS_REGION"] = Environment.GetEnvironmentVariable("AWS_REGION") ?? "not-set",
            ["PORT"] = Environment.GetEnvironmentVariable("PORT") ?? "5000"
        };

        return Ok(new
        {
            application = "GuideApi",
            runtime = RuntimeInformation.FrameworkDescription,
            operating_system = RuntimeInformation.OSDescription,
            architecture = RuntimeInformation.ProcessArchitecture.ToString(),
            machine_name = Environment.MachineName,
            environment = safeEnvironment
        });
    }
}
